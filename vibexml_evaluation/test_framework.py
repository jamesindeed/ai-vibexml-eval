#!/usr/bin/env python3
"""
Framework Test Script

Quick test to verify the LLML evaluation framework is working correctly.
This script runs a minimal evaluation to check all components.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from vibexml_evaluation import LLMLEvaluator, PydanticAIProvider, TestCaseDataset


async def test_framework():
    """Test the framework with a single test case."""
    print("🧪 Testing LLML Evaluation Framework")
    print("=" * 40)

    # Check API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY not set")
        print("Please set your API key: export OPENROUTER_API_KEY='your-key'")
        return False

    try:
        model = "anthropic/claude-3.5-haiku"
        print(f"🤖 Using model: {model}")

        provider = PydanticAIProvider(model=model)
        print("✅ Provider created")

        evaluator = LLMLEvaluator(provider)
        print("✅ Evaluator created")

        test_cases = TestCaseDataset.get_all_cases()[:1]
        print(f"📋 Testing with: {test_cases[0].name}")

        results = await evaluator.run_evaluation(test_cases)
        print("✅ Evaluation completed")

        assert len(results["ab_results"]) == 1
        assert len(results["judgments"]) == 1
        assert "analysis" in results

        judgment = results["judgments"][0]
        print(f"🏆 Winner: {judgment.winner}")
        print(f"📊 Confidence: {judgment.confidence:.1f}%")
        print(
            f"📈 Score difference: {judgment.vibexml_score - judgment.raw_text_score:+.1f}"
        )

        print()
        print("✅ Framework test PASSED!")
        print("🚀 Ready for full evaluation")
        return True

    except Exception as e:
        print(f"❌ Framework test FAILED: {e}")
        print()
        print("🔍 Check:")
        print("   • pydantic-ai installation: pip install pydantic-ai-slim[openai]")
        print("   • API key validity")
        print("   • Internet connection")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_framework())
    sys.exit(0 if success else 1)
