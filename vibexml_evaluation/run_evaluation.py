#!/usr/bin/env python3
"""
LLML Evaluation Runner

Main entry point for running structured vs unstructured data formatting evaluation
using LLM-as-a-judge methodology.

This script provides a clean command-line interface for conducting research-grade
evaluations of prompt formatting strategies.
"""

import argparse
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from vibexml_evaluation import LLMLEvaluator, PydanticAIProvider, TestCaseDataset
from vibexml_evaluation.academic_enhancements import StatisticalAnalysisReporter


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description="LLML Evaluation: Structured vs Unstructured Data Formatting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic evaluation with default models
  python run_evaluation.py
  
  # Use specific models for response generation and judging
  python run_evaluation.py --model anthropic/claude-3.5-sonnet --judge openai/gpt-4o
  
  # Academic analysis with statistical rigor
  python run_evaluation.py --model anthropic/claude-3.5-sonnet --academic
  
  # Quick test with a specific model
  python run_evaluation.py --model anthropic/claude-4-sonnet-20250514 --single nested_conditional_logic
  
  # Fast evaluation for development
  python run_evaluation.py --model anthropic/claude-3.5-haiku --cases 2

Recommended model combinations:
  • anthropic/claude-3.5-sonnet + openai/gpt-4o (different perspectives)
  • openai/gpt-4o + anthropic/claude-3.5-sonnet (reverse perspective)
  • anthropic/claude-3.5-haiku (fast, cost-effective for development)
  
For research papers, use different model families for generation vs judging.
Add --academic flag for publication-ready statistical analysis.
        """,
    )

    parser.add_argument(
        "--model",
        type=str,
        default="anthropic/claude-3.5-sonnet",
        help="OpenRouter model for response generation (default: anthropic/claude-3.5-sonnet)",
    )

    parser.add_argument(
        "--judge",
        type=str,
        help="OpenRouter model for judging (default: same as --model)",
    )

    parser.add_argument(
        "--cases",
        type=int,
        help="Number of test cases to run (default: all)",
    )

    parser.add_argument(
        "--single",
        type=str,
        help="Run single test case by name (for debugging)",
    )

    parser.add_argument(
        "--list-cases",
        action="store_true",
        help="List available test cases and exit",
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List recommended models and exit",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Custom output filename (default: auto-generated)",
    )

    parser.add_argument(
        "--academic",
        action="store_true",
        help="Include academic statistical analysis for publication",
    )

    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible judge evaluation order (optional)",
    )

    return parser.parse_args()


def check_api_key() -> bool:
    """Check if OpenRouter API key is configured."""
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Error: OPENROUTER_API_KEY environment variable not set")
        print()
        print("Please set your API key:")
        print("  export OPENROUTER_API_KEY='your-api-key-here'")
        print()
        print("Get your API key from: https://openrouter.ai/keys")
        return False
    return True


def list_models() -> None:
    """Display recommended models for evaluation."""
    print("🤖 Recommended Models for LLML Evaluation:")
    print()

    models = [
        ("anthropic/claude-3.5-sonnet", "Excellent balance, good reasoning"),
        ("openai/gpt-4o", "Strong analytical capabilities"),
        ("anthropic/claude-3.5-haiku", "Fast and cost-effective"),
        ("openai/gpt-4o-mini", "Efficient alternative to GPT-4o"),
        ("meta-llama/llama-3.3-70b-instruct", "Open source option"),
        ("google/gemini-2.0-flash-exp", "Google's latest model"),
        ("qwen/qwen-2.5-coder-32b-instruct", "Code-specialized model"),
        ("anthropic/claude-4-sonnet-20250514", "Latest Claude model"),
    ]

    for model, description in models:
        print(f"  {model:<40} - {description}")

    print()
    print("💡 For research-grade evaluation:")
    print("   • Use different model families for generation vs judging")
    print("   • Example: --model anthropic/claude-3.5-sonnet --judge openai/gpt-4o")
    print("   • This reduces potential bias from using the same model family")


def list_test_cases() -> None:
    """Display available test cases."""
    print("📋 Available Test Cases:")
    print()

    test_cases = TestCaseDataset.get_all_cases()
    for i, tc in enumerate(test_cases, 1):
        print(f"{i}. {tc.name}")
        print(f"   📝 {tc.description}")
        print(f"   🎯 Why structure helps: {tc.why_structure_helps}")
        print(f"   ✅ Expected advantages: {len(tc.expected_advantages)} criteria")
        print()


def print_academic_analysis(statistical_summary: dict) -> None:
    """Print objective statistical analysis for research evaluation."""
    print()
    print("📊 STATISTICAL ANALYSIS")
    print("=" * 60)
    print()

    # Study Design
    design = statistical_summary["study_design"]
    print("🔬 Study Design:")
    print(f"   Method: {design['method']}")
    print(f"   Comparison: {design['comparison']}")
    print(f"   Design Type: {design['design_type']}")
    print(f"   Sample Size: N = {design['sample_size']}")
    print(f"   Evaluation Criteria: {design['evaluation_criteria']}")
    print(f"   Blind Evaluation: {'✅' if design['blind_evaluation'] else '❌'}")
    print()

    # Descriptive Statistics
    desc = statistical_summary["descriptive_statistics"]
    print("📈 Descriptive Statistics:")
    print("   Raw Text:")
    print(
        f"      M = {desc['raw_text']['mean']:.1f}, SD = {desc['raw_text']['std']:.1f}"
    )
    print(
        f"      Median = {desc['raw_text']['median']:.1f}, Range = [{desc['raw_text']['min']:.1f}, {desc['raw_text']['max']:.1f}]"
    )
    print("   VibeXML:")
    print(f"      M = {desc['vibexml']['mean']:.1f}, SD = {desc['vibexml']['std']:.1f}")
    print(
        f"      Median = {desc['vibexml']['median']:.1f}, Range = [{desc['vibexml']['min']:.1f}, {desc['vibexml']['max']:.1f}]"
    )
    print("   Difference:")
    print(
        f"      M = {desc['difference']['mean']:+.1f}, SD = {desc['difference']['std']:.1f}"
    )
    print()

    # Inferential Statistics
    stats_section = statistical_summary["inferential_statistics"]

    # T-test results
    ttest = stats_section["paired_t_test"]
    print("🎯 Paired t-test:")
    print(f"   t({ttest['degrees_freedom']}) = {ttest['t_statistic']:.3f}")
    print(f"   p = {ttest['p_value']:.6f}")
    print(
        f"   Statistically significant: {'Yes' if ttest['significant'] else 'No'} (α = 0.05)"
    )
    ci_low, ci_high = ttest["confidence_interval"]
    print(f"   95% CI: [{ci_low:.1f}, {ci_high:.1f}]")
    print()

    # Effect Size
    effect = stats_section["effect_size"]
    print("📏 Effect Size:")
    print(
        f"   Cohen's d = {effect['cohens_d']:.3f} ({effect['effect_size_interpretation']})"
    )
    print(f"   Mean difference = {effect['mean_difference']:+.1f} points")
    if effect["pooled_std"] > 0:
        print(f"   Pooled SD = {effect['pooled_std']:.2f}")
    print()

    # Power Analysis
    if (
        "power_analysis" in stats_section
        and stats_section["power_analysis"]["observed_power"]
    ):
        power = stats_section["power_analysis"]
        print("⚡ Power Analysis:")
        print(f"   Observed power = {power['observed_power']:.3f}")
        print(f"   Effect size used = {power['effect_size_used']:.3f}")
        print(f"   Alpha level = {power['alpha_level']}")
        print()

    # Categorical Outcomes
    categorical = statistical_summary["categorical_outcomes"]
    print("🏆 Categorical Outcomes:")
    print(
        f"   VibeXML wins: {categorical['vibexml_wins']}/{categorical['total_cases']} ({categorical['vibexml_win_rate']:.1%})"
    )
    print(
        f"   Raw text wins: {categorical['raw_text_wins']}/{categorical['total_cases']} ({categorical['raw_text_win_rate']:.1%})"
    )
    print(
        f"   Ties: {categorical['ties']}/{categorical['total_cases']} ({categorical['tie_rate']:.1%})"
    )

    binomial = categorical["binomial_test"]
    print(f"   Binomial test: p = {binomial['p_value']:.6f}")
    print(
        f"   Win rate significantly different from chance: {'Yes' if binomial['statistically_significant'] else 'No'}"
    )
    print(f"   Null hypothesis: {binomial['null_hypothesis']}")
    print()


async def main() -> None:
    """Main evaluation function."""
    args = parse_arguments()

    # Handle info commands
    if args.list_models:
        list_models()
        return

    if args.list_cases:
        list_test_cases()
        return

    # Check API key
    if not check_api_key():
        return

    # Set up models
    response_model = args.model
    judge_model = args.judge or response_model

    print("🚀 LLML Evaluation Framework")
    print("=" * 50)
    print(f"📊 Response model: {response_model}")
    print(f"⚖️  Judge model: {judge_model}")
    print()

    try:
        # Create AI providers
        print("🔧 Initializing AI providers...")
        response_provider = PydanticAIProvider(model=response_model)

        if judge_model == response_model:
            judge_provider = response_provider
            print("✅ Using same provider for judging (memory efficient)")
        else:
            judge_provider = PydanticAIProvider(model=judge_model)
            print("✅ Created separate judge provider")

        # Create evaluator
        evaluator = LLMLEvaluator(
            response_provider, judge_provider, random_seed=args.seed
        )

        # Select test cases
        all_test_cases = TestCaseDataset.get_all_cases()

        if args.single:
            test_cases = [tc for tc in all_test_cases if tc.name == args.single]
            if not test_cases:
                print(f"❌ Test case '{args.single}' not found")
                print("Available test cases:")
                for tc in all_test_cases:
                    print(f"  - {tc.name}")
                return
            print(f"🎯 Running single test case: {args.single}")
        elif args.cases:
            test_cases = all_test_cases[: args.cases]
            print(f"🔍 Running {len(test_cases)} of {len(all_test_cases)} test cases")
        else:
            test_cases = all_test_cases
            print(f"📊 Running all {len(test_cases)} test cases")

        print()

        # Run evaluation
        results = await evaluator.run_evaluation(test_cases)

        # Print regular summary
        evaluator.print_summary(results)

        # Add academic analysis if requested
        if args.academic:
            try:
                print()
                print("🔬 Running Academic Statistical Analysis...")

                # Generate academic analysis
                statistical_reporter = StatisticalAnalysisReporter(results)
                academic_summary = statistical_reporter.generate_statistical_summary()

                # Print academic results
                print_academic_analysis(academic_summary)

                # Add to results for saving
                results["academic_analysis"] = academic_summary

            except Exception as e:
                print(f"❌ Academic analysis failed: {e}")
                print("   Continuing with regular results...")

        # Save results (now includes academic analysis if --academic was used)
        filename = evaluator.save_results(results, args.output)

        print()
        print(f"📁 Detailed results saved to: {filename}")
        print("🎉 Evaluation complete!")

    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        print()
        print("🔍 Common issues:")
        print(
            "   • Ensure pydantic-ai is installed: pip install pydantic-ai-slim[openai]"
        )
        print("   • Verify your OPENROUTER_API_KEY is valid")
        print("   • Check model names are correct (use --list-models)")
        sys.exit(1)


def cli_main() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
