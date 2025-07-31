"""
LLM-as-Judge Evaluation System

This module implements an LLM-based judge that objectively evaluates which response
better demonstrates understanding and utilization of structured data.
"""

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field

from .providers import PydanticAIProvider


class CriteriaScores(BaseModel):
    """Individual criteria scores for detailed analysis."""

    accuracy_completeness: int = Field(
        ge=60,
        le=95,
        description="How well the response addresses all aspects of the task",
    )
    structured_data_utilization: int = Field(
        ge=60,
        le=95,
        description="Understanding of complex relationships and hierarchies",
    )
    precision_specificity: int = Field(
        ge=60, le=95, description="References to specific values and parameters"
    )
    logical_flow_organization: int = Field(
        ge=60, le=95, description="Organization and logical reasoning quality"
    )
    contextual_understanding: int = Field(
        ge=60, le=95, description="Awareness of interconnected contexts"
    )


class StructuredJudgment(BaseModel):
    """Structured judgment response for academic evaluation."""

    # Winner determination
    winner: Literal["A", "B", "TIE"] = Field(
        description="Which response is better: A (unstructured), B (structured), or TIE"
    )

    # Detailed scores for each response
    response_a_scores: CriteriaScores = Field(
        description="Detailed scores for Response A (unstructured)"
    )
    response_b_scores: CriteriaScores = Field(
        description="Detailed scores for Response B (structured)"
    )

    # Overall scores (calculated from criteria)
    response_a_overall: int = Field(
        ge=60, le=95, description="Overall score for Response A"
    )
    response_b_overall: int = Field(
        ge=60, le=95, description="Overall score for Response B"
    )

    # Confidence and reasoning
    confidence: int = Field(
        ge=50, le=100, description="Confidence in this judgment (50-100)"
    )
    reasoning: str = Field(
        min_length=50,
        description="Detailed explanation of the judgment specific to this test case",
    )

    # Key differences observed
    main_advantages: List[str] = Field(
        max_items=3, description="Top 2-3 specific advantages of the winning response"
    )


@dataclass
class JudgmentResult:
    """
    Result from LLM judge evaluation.

    Attributes:
        test_case_name: Name of the test case being judged
        winner: Which format won ("raw_text", "vibexml", or "tie")
        confidence: Judge's confidence in the decision (0-100)
        raw_text_score: Overall score for raw text response (0-100)
        vibexml_score: Overall score for VibeXML response (0-100)
        reasoning: Judge's explanation for the decision
        criteria_scores: Detailed scores by evaluation criteria
    """

    test_case_name: str
    winner: str
    confidence: float
    raw_text_score: float
    vibexml_score: float
    reasoning: str
    criteria_scores: Dict[str, Dict[str, float]]


class LLMJudge:
    """
    LLM-based judge for evaluating response quality in structured vs unstructured comparisons.

    This judge evaluates responses across multiple criteria to determine which format
    (structured or unstructured) produces higher quality AI responses.
    """

    def __init__(self, judge_provider: PydanticAIProvider, random_seed: int = None):
        """
        Initialize the LLM judge.

        Args:
            judge_provider: The AI provider to use for judging
            random_seed: Optional seed for reproducible randomization of response order
        """
        self.judge_provider = judge_provider
        if random_seed is not None:
            random.seed(random_seed)

    def create_judgment_prompt(
        self,
        test_case_name: str,
        task: str,
        expected_advantages: List[str],
        raw_text_response: str,
        vibexml_response: str,
    ) -> tuple[str, bool]:
        """
        Create a comprehensive prompt for the judge to evaluate responses.

        This prompt instructs the judge to evaluate responses across multiple
        criteria and provide detailed reasoning for the decision.

        Returns:
            Tuple of (prompt_text, raw_text_is_a) where raw_text_is_a indicates
            whether raw_text_response was assigned as Response A (True) or B (False)
        """
        # Randomly assign which response gets A vs B label to prevent bias
        raw_text_is_a = random.choice([True, False])

        if raw_text_is_a:
            response_a = raw_text_response
            response_b = vibexml_response
            response_a_label = "Response A"
            response_b_label = "Response B"
        else:
            response_a = vibexml_response
            response_b = raw_text_response
            response_a_label = "Response A"
            response_b_label = "Response B"

        prompt = f"""You are an expert evaluator assessing AI response quality. Compare two responses to the same task and determine which demonstrates better understanding and utilization of the provided information.

EVALUATION CONTEXT: Test case "{test_case_name}"
TASK: {task}

KEY EVALUATION FACTORS:
{chr(10).join(f"- {adv}" for adv in expected_advantages)}

{response_a_label}:
{response_a}

{response_b_label}:
{response_b}

EVALUATION CRITERIA:
Score both responses on each criterion (60-95 scale):

1. **Accuracy & Completeness**: How well each addresses all aspects of the task
2. **Structured Data Utilization**: How well each demonstrates understanding of complex relationships
3. **Precision & Specificity**: Which references specific values/parameters more effectively  
4. **Logical Flow & Organization**: Which is better organized with clearer reasoning
5. **Contextual Understanding**: Which shows better awareness of interconnected contexts

SCORING GUIDANCE:
- Use realistic score ranges (most scores 70-90, exceptional cases can go 60-69 or 91-95)
- Focus on concrete, observable differences between responses
- Confidence should reflect how clear the differences are (50-100)
- Provide specific examples from the responses in your reasoning

Your response will be validated for proper structure and scoring ranges."""

        return prompt, raw_text_is_a

    async def judge_responses(
        self,
        test_case_name: str,
        task: str,
        expected_advantages: List[str],
        raw_text_response: str,
        vibexml_response: str,
    ) -> JudgmentResult:
        """
        Have the LLM judge evaluate which response is better.

        Args:
            test_case_name: Name of the test case
            task: The task description
            expected_advantages: Expected advantages of structured format
            raw_text_response: Response from unstructured prompt
            vibexml_response: Response from structured prompt

        Returns:
            Judgment result with scores and reasoning
        """
        judgment_prompt, raw_text_is_a = self.create_judgment_prompt(
            test_case_name,
            task,
            expected_advantages,
            raw_text_response,
            vibexml_response,
        )

        print(f"    Judging responses for {test_case_name}...")

        try:
            # Get structured judgment from LLM using Pydantic AI
            structured_judgment = (
                await self.judge_provider.generate_structured_response(
                    judgment_prompt, StructuredJudgment
                )
            )

            # Map winner to our format based on randomization
            if raw_text_is_a:
                # raw_text was Response A, vibexml was Response B
                winner_map = {"A": "raw_text", "B": "vibexml", "TIE": "tie"}
                raw_text_score = structured_judgment.response_a_overall
                vibexml_score = structured_judgment.response_b_overall
                raw_text_criteria = structured_judgment.response_a_scores
                vibexml_criteria = structured_judgment.response_b_scores
            else:
                # vibexml was Response A, raw_text was Response B
                winner_map = {"A": "vibexml", "B": "raw_text", "TIE": "tie"}
                raw_text_score = structured_judgment.response_b_overall
                vibexml_score = structured_judgment.response_a_overall
                raw_text_criteria = structured_judgment.response_b_scores
                vibexml_criteria = structured_judgment.response_a_scores

            winner = winner_map[structured_judgment.winner]

            # Convert structured scores to our format
            criteria_scores = {
                "accuracy_completeness": {
                    "raw_text": raw_text_criteria.accuracy_completeness,
                    "vibexml": vibexml_criteria.accuracy_completeness,
                },
                "structured_data_utilization": {
                    "raw_text": raw_text_criteria.structured_data_utilization,
                    "vibexml": vibexml_criteria.structured_data_utilization,
                },
                "precision_specificity": {
                    "raw_text": raw_text_criteria.precision_specificity,
                    "vibexml": vibexml_criteria.precision_specificity,
                },
                "logical_flow_organization": {
                    "raw_text": raw_text_criteria.logical_flow_organization,
                    "vibexml": vibexml_criteria.logical_flow_organization,
                },
                "contextual_understanding": {
                    "raw_text": raw_text_criteria.contextual_understanding,
                    "vibexml": vibexml_criteria.contextual_understanding,
                },
            }

            return JudgmentResult(
                test_case_name=test_case_name,
                winner=winner,
                confidence=structured_judgment.confidence,
                raw_text_score=raw_text_score,
                vibexml_score=vibexml_score,
                reasoning=structured_judgment.reasoning,
                criteria_scores=criteria_scores,
            )

        except Exception as e:
            print(f"    Warning: Structured judgment failed for {test_case_name}: {e}")
            print("    Falling back to simple heuristic...")

            # Fallback: simple heuristic
            return self._fallback_judgment(
                test_case_name, raw_text_response, vibexml_response
            )

    def _fallback_judgment(
        self, test_case_name: str, raw_text_response: str, vibexml_response: str
    ) -> JudgmentResult:
        """
        Fallback judgment when JSON parsing fails.

        Uses simple heuristics to make a basic comparison.
        """
        # Simple length-based scoring as fallback
        raw_text_score = min(len(raw_text_response.split()) / 10 * 5, 100)
        vibexml_score = min(len(vibexml_response.split()) / 10 * 5, 100)

        if abs(raw_text_score - vibexml_score) < 5:
            winner = "tie"
        else:
            winner = "raw_text" if raw_text_score > vibexml_score else "vibexml"

        return JudgmentResult(
            test_case_name=test_case_name,
            winner=winner,
            confidence=50.0,  # Low confidence for fallback
            raw_text_score=raw_text_score,
            vibexml_score=vibexml_score,
            reasoning="Fallback judgment due to parsing error",
            criteria_scores={
                "fallback": {"raw_text": raw_text_score, "vibexml": vibexml_score}
            },
        )


class JudgmentAnalyzer:
    """Analyzes judgment results across multiple test cases."""

    @staticmethod
    def analyze_judgments(
        judgments: List[JudgmentResult], test_cases: List = None
    ) -> Dict[str, Any]:
        """
        Analyze patterns in judgments across all test cases.

        Args:
            judgments: List of judgment results
            test_cases: Optional list of test cases for category analysis

        Returns:
            Comprehensive analysis of results including win rates and score breakdowns
        """
        total_tests = len(judgments)
        vibexml_wins = sum(1 for j in judgments if j.winner == "vibexml")
        raw_text_wins = sum(1 for j in judgments if j.winner == "raw_text")
        ties = sum(1 for j in judgments if j.winner == "tie")

        # Calculate average scores
        avg_raw_text_score = sum(j.raw_text_score for j in judgments) / total_tests
        avg_vibexml_score = sum(j.vibexml_score for j in judgments) / total_tests
        avg_confidence = sum(j.confidence for j in judgments) / total_tests

        # Analyze criteria
        criteria_analysis = {}
        if judgments and judgments[0].criteria_scores:
            for criterion in judgments[0].criteria_scores.keys():
                raw_scores = [
                    j.criteria_scores[criterion]["raw_text"]
                    for j in judgments
                    if criterion in j.criteria_scores
                ]
                vibexml_scores = [
                    j.criteria_scores[criterion]["vibexml"]
                    for j in judgments
                    if criterion in j.criteria_scores
                ]

                if raw_scores and vibexml_scores:
                    criteria_analysis[criterion] = {
                        "raw_text_avg": sum(raw_scores) / len(raw_scores),
                        "vibexml_avg": sum(vibexml_scores) / len(vibexml_scores),
                        "vibexml_advantage": (sum(vibexml_scores) / len(vibexml_scores))
                        - (sum(raw_scores) / len(raw_scores)),
                    }

        # Analyze by category if test cases provided
        category_analysis = {}
        if test_cases:
            # Create mapping from test case name to category
            case_categories = {tc.name: tc.category for tc in test_cases}

            # Group judgments by category
            categories = {}
            for judgment in judgments:
                category = case_categories.get(judgment.test_case_name, "unknown")
                if category not in categories:
                    categories[category] = []
                categories[category].append(judgment)

            # Analyze each category
            for category, cat_judgments in categories.items():
                if not cat_judgments:
                    continue

                cat_total = len(cat_judgments)
                cat_vibexml_wins = sum(
                    1 for j in cat_judgments if j.winner == "vibexml"
                )
                cat_raw_text_wins = sum(
                    1 for j in cat_judgments if j.winner == "raw_text"
                )
                cat_ties = sum(1 for j in cat_judgments if j.winner == "tie")

                cat_avg_raw = sum(j.raw_text_score for j in cat_judgments) / cat_total
                cat_avg_vibexml = (
                    sum(j.vibexml_score for j in cat_judgments) / cat_total
                )

                category_analysis[category] = {
                    "total_tests": cat_total,
                    "vibexml_wins": cat_vibexml_wins,
                    "raw_text_wins": cat_raw_text_wins,
                    "ties": cat_ties,
                    "vibexml_win_rate": cat_vibexml_wins / cat_total * 100,
                    "raw_text_win_rate": cat_raw_text_wins / cat_total * 100,
                    "avg_raw_text_score": cat_avg_raw,
                    "avg_vibexml_score": cat_avg_vibexml,
                    "vibexml_advantage": cat_avg_vibexml - cat_avg_raw,
                    "test_cases": [j.test_case_name for j in cat_judgments],
                }

        return {
            "summary": {
                "total_tests": total_tests,
                "vibexml_wins": vibexml_wins,
                "raw_text_wins": raw_text_wins,
                "ties": ties,
                "vibexml_win_rate": vibexml_wins / total_tests * 100,
                "raw_text_win_rate": raw_text_wins / total_tests * 100,
            },
            "average_scores": {
                "raw_text": avg_raw_text_score,
                "vibexml": avg_vibexml_score,
                "vibexml_advantage": avg_vibexml_score - avg_raw_text_score,
                "average_confidence": avg_confidence,
            },
            "criteria_analysis": criteria_analysis,
            "category_analysis": category_analysis,
            "detailed_results": [
                {
                    "test_case": j.test_case_name,
                    "winner": j.winner,
                    "confidence": j.confidence,
                    "score_difference": j.vibexml_score - j.raw_text_score,
                    "reasoning": j.reasoning,
                }
                for j in judgments
            ],
        }

    @staticmethod
    def print_analysis(analysis: Dict[str, Any]) -> None:
        """Print a formatted analysis of the judgment results."""
        summary = analysis["summary"]
        scores = analysis["average_scores"]

        print("🏆 JUDGMENT ANALYSIS RESULTS")
        print("=" * 50)
        print()

        print("📊 Win/Loss Summary:")
        print(
            f"  VibeXML wins: {summary['vibexml_wins']}/{summary['total_tests']} ({summary['vibexml_win_rate']:.1f}%)"
        )
        print(
            f"  Raw Text wins: {summary['raw_text_wins']}/{summary['total_tests']} ({summary['raw_text_win_rate']:.1f}%)"
        )
        print(
            f"  Ties: {summary['ties']}/{summary['total_tests']} ({summary['ties'] / summary['total_tests'] * 100:.1f}%)"
        )
        print()

        print("📈 Average Scores:")
        print(f"  Raw Text: {scores['raw_text']:.1f}/100")
        print(f"  VibeXML: {scores['vibexml']:.1f}/100")
        print(f"  VibeXML Advantage: {scores['vibexml_advantage']:+.1f} points")
        print(f"  Judge Confidence: {scores['average_confidence']:.1f}%")
        print()

        if analysis["criteria_analysis"]:
            print("🔍 Criteria Breakdown:")
            for criterion, data in analysis["criteria_analysis"].items():
                advantage = data["vibexml_advantage"]
                print(f"  {criterion.replace('_', ' ').title()}:")
                print(f"    Raw Text: {data['raw_text_avg']:.1f}")
                print(f"    VibeXML: {data['vibexml_avg']:.1f}")
                print(
                    f"    Advantage: {advantage:+.1f} {'✅' if advantage > 5 else '❌' if advantage < -5 else '➖'}"
                )
            print()

        if analysis["category_analysis"]:
            print("📂 Category Analysis:")
            for category, data in analysis["category_analysis"].items():
                advantage = data["vibexml_advantage"]
                win_rate = data["vibexml_win_rate"]
                print(
                    f"  {category.replace('_', ' ').title()} ({data['total_tests']} tests):"
                )
                print(
                    f"    VibeXML Win Rate: {win_rate:.1f}% ({data['vibexml_wins']}/{data['total_tests']})"
                )
                print(f"    Score Advantage: {advantage:+.1f} points")
                performance_emoji = (
                    "🔥" if advantage > 3 else "❌" if advantage < -2 else "⚖️"
                )
                expected_emoji = (
                    "✅"
                    if category == "structured_advantage" and advantage > 0
                    else (
                        "⚠️"
                        if category in ["creative", "adversarial"] and advantage > 0
                        else "✅"
                    )
                )
                print(
                    f"    Performance: {performance_emoji} Expected: {expected_emoji}"
                )
            print()

        print("📋 Individual Results:")
        for result in analysis["detailed_results"]:
            winner_emoji = {"vibexml": "🥇", "raw_text": "🥈", "tie": "🤝"}
            print(
                f"  {result['test_case']}: {winner_emoji.get(result['winner'], '❓')} {result['winner']}"
            )
            print(
                f"    Score difference: {result['score_difference']:+.1f} (confidence: {result['confidence']:.0f}%)"
            )
            print(f"    Reasoning: {result['reasoning'][:100]}...")
            print()
