"""
LLML Evaluation Orchestrator

This module provides the main evaluation orchestrator that coordinates the complete
pipeline: response generation, LLM judging, and result analysis.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

from .judge import JudgmentAnalyzer, LLMJudge
from .providers import PydanticAIProvider
from .runner import ABTestRunner
from .test_cases import StructuredTestCase


class LLMLEvaluator:
    """
    Main orchestrator for LLML evaluation pipeline.

    This class coordinates the complete evaluation process:
    1. Generate responses with both structured and unstructured formats
    2. Use LLM judge to evaluate response quality
    3. Analyze results across all test cases
    4. Save comprehensive results for further analysis
    """

    def __init__(
        self,
        response_provider: PydanticAIProvider,
        judge_provider: Optional[PydanticAIProvider] = None,
        random_seed: Optional[int] = None,
    ):
        """
        Initialize the evaluation orchestrator.

        Args:
            response_provider: AI provider for generating responses
            judge_provider: AI provider for judging (defaults to response_provider)
            random_seed: Optional seed for reproducible randomization of judge evaluations
        """
        self.response_provider = response_provider
        self.judge_provider = judge_provider or response_provider

        self.ab_runner = ABTestRunner(response_provider)
        self.judge = LLMJudge(self.judge_provider, random_seed=random_seed)

    async def run_evaluation(self, test_cases: List[StructuredTestCase]) -> Dict:
        """
        Run the complete evaluation pipeline.

        Args:
            test_cases: List of test cases to evaluate

        Returns:
            Complete evaluation results including responses, judgments, and analysis
        """
        print("🔬 LLML EVALUATION: Structured vs Unstructured Data Formatting")
        print("=" * 70)
        print(f"📊 Test cases: {len(test_cases)}")
        print(f"🤖 Response model: {self.response_provider.model_name}")
        print(f"⚖️  Judge model: {self.judge_provider.model_name}")
        print()

        # Step 1: Generate responses with both formats
        print("📋 STEP 1: Generating responses with both formats...")
        ab_results = await self.ab_runner.run_all_tests(test_cases)
        print("✅ Response generation complete!")
        print()

        # Step 2: Judge all responses
        print("⚖️  STEP 2: Judging response quality...")
        judgments = []

        for ab_result in ab_results:
            # Find the corresponding test case for expected advantages
            test_case = next(
                tc for tc in test_cases if tc.name == ab_result.test_case_name
            )

            judgment = await self.judge.judge_responses(
                test_case_name=ab_result.test_case_name,
                task=test_case.task,
                expected_advantages=test_case.expected_advantages,
                raw_text_response=ab_result.raw_text_response,
                vibexml_response=ab_result.vibexml_response,
            )
            judgments.append(judgment)

        print("✅ Judging complete!")
        print()

        # Step 3: Analyze results
        print("📊 STEP 3: Analyzing results...")
        analysis = JudgmentAnalyzer.analyze_judgments(judgments, test_cases)

        results = {
            "ab_results": ab_results,
            "judgments": judgments,
            "analysis": analysis,
            "metadata": {
                "response_model": self.response_provider.model_name,
                "judge_model": self.judge_provider.model_name,
                "test_cases_evaluated": [tc.name for tc in test_cases],
                "evaluation_timestamp": datetime.now().isoformat(),
            },
        }

        print("✅ Analysis complete!")
        return results

    def save_results(self, results: Dict, filename: Optional[str] = None) -> str:
        """
        Save evaluation results to file.

        Args:
            results: Complete evaluation results
            filename: Optional custom filename

        Returns:
            The filename where results were saved
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            response_model = results["metadata"]["response_model"]
            judge_model = results["metadata"]["judge_model"]

            # Sanitize model names for filename
            safe_response = (
                response_model.replace("/", "_").replace("-", "_").replace(":", "_")
            )
            safe_judge = (
                judge_model.replace("/", "_").replace("-", "_").replace(":", "_")
            )

            if safe_response == safe_judge:
                filename = f"llml_evaluation_{safe_response}_{timestamp}.json"
            else:
                filename = f"llml_evaluation_{safe_response}_judge_{safe_judge}_{timestamp}.json"

        # Convert to serializable format
        serializable_data = {
            "metadata": {
                "test_type": "llml_structured_vs_unstructured",
                "framework_version": "1.0.0",
                **results["metadata"],
            },
            "ab_test_results": [
                {
                    "test_case_name": r.test_case_name,
                    "raw_text_prompt": r.raw_text_prompt,
                    "vibexml_prompt": r.vibexml_prompt,
                    "raw_text_response": r.raw_text_response,
                    "vibexml_response": r.vibexml_response,
                    "raw_text_length": r.raw_text_length,
                    "vibexml_length": r.vibexml_length,
                }
                for r in results["ab_results"]
            ],
            "judgments": [
                {
                    "test_case_name": j.test_case_name,
                    "winner": j.winner,
                    "confidence": j.confidence,
                    "raw_text_score": j.raw_text_score,
                    "vibexml_score": j.vibexml_score,
                    "reasoning": j.reasoning,
                    "criteria_scores": j.criteria_scores,
                }
                for j in results["judgments"]
            ],
            "analysis": results["analysis"],
        }

        with open(filename, "w") as f:
            json.dump(serializable_data, f, indent=2)

        print(f"💾 Results saved to: {filename}")
        return filename

    def print_summary(self, results: Dict) -> None:
        """
        Print a summary of the evaluation results.

        Args:
            results: Complete evaluation results
        """
        # Print detailed analysis
        JudgmentAnalyzer.print_analysis(results["analysis"])

        # Print final verdict
        analysis = results["analysis"]
        vibexml_wins = analysis["summary"]["vibexml_wins"]
        total_tests = analysis["summary"]["total_tests"]
        advantage = analysis["average_scores"]["vibexml_advantage"]

        print()
        print("🎯 FINAL VERDICT:")
        if vibexml_wins > total_tests / 2:
            print(
                f"✅ VibeXML (structured) wins! "
                f"({vibexml_wins}/{total_tests} wins, +{advantage:.1f} avg score advantage)"
            )
            print(
                "   📈 Structured formatting shows measurable advantages for AI comprehension."
            )
        elif vibexml_wins < total_tests / 2:
            raw_wins = analysis["summary"]["raw_text_wins"]
            print(f"❌ Raw text (unstructured) wins! ({raw_wins}/{total_tests} wins)")
            print(
                "   📉 Structured formatting does not show clear advantages in these tests."
            )
        else:
            print(f"🤝 Tie! ({vibexml_wins}/{total_tests} wins each)")
            print("   ➖ No clear advantage detected for either format.")

        print()
        print("📊 For more robust results, consider:")
        print("   • Testing with additional model families")
        print("   • Expanding the test case dataset")
        print("   • Using multiple judge models for consensus")
        print("   • Analyzing specific criteria where structured format excels")
