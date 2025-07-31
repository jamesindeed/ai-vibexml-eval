"""
A/B Test Runner for LLML Evaluation

This module handles the generation of prompts in both structured (VibeXML) and
unstructured (raw text) formats, and collects AI responses for comparison.
"""

import os
import sys
from dataclasses import dataclass
from typing import Any, Dict

# Add the parent directory to path to import zenbase_llml
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "py", "src")
)

from zenbase_llml import llml

from .providers import PydanticAIProvider
from .test_cases import StructuredTestCase


@dataclass
class ABTestResult:
    """
    Results from A/B testing one case with both formatting approaches.

    Attributes:
        test_case_name: Name of the test case
        raw_text_prompt: The unstructured prompt
        vibexml_prompt: The structured (VibeXML) prompt
        raw_text_response: AI response to raw text prompt
        vibexml_response: AI response to VibeXML prompt
        raw_text_length: Character count of raw text prompt
        vibexml_length: Character count of VibeXML prompt
    """

    test_case_name: str
    raw_text_prompt: str
    vibexml_prompt: str
    raw_text_response: str
    vibexml_response: str
    raw_text_length: int
    vibexml_length: int


class PromptFormatter:
    """Handles conversion between structured data and different prompt formats."""

    @staticmethod
    def to_raw_text(test_case: StructuredTestCase) -> str:
        """
        Convert structured data to traditional string concatenation format.

        This creates an unstructured representation that concatenates
        the data hierarchically but without explicit markup.
        """

        def format_dict_as_text(data: Dict[str, Any], indent: int = 0) -> str:
            """Recursively format dictionary as readable text."""
            result = []
            spaces = "  " * indent

            for key, value in data.items():
                if isinstance(value, dict):
                    result.append(f"{spaces}{key}:")
                    result.append(format_dict_as_text(value, indent + 1))
                elif isinstance(value, list):
                    result.append(f"{spaces}{key}:")
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            result.append(f"{spaces}  {i + 1}.")
                            result.append(format_dict_as_text(item, indent + 2))
                        else:
                            result.append(f"{spaces}  - {item}")
                else:
                    result.append(f"{spaces}{key}: {value}")

            return "\n".join(filter(None, result))

        # Format the data section
        data_section = format_dict_as_text(test_case.data)

        # Combine with task
        prompt = f"""Task: {test_case.task}

Data:
{data_section}

Please analyze this information and provide a detailed response."""

        return prompt

    @staticmethod
    def to_vibexml(test_case: StructuredTestCase) -> str:
        """
        Convert structured data to VibeXML format using LLML.

        This creates a structured XML-like representation that preserves
        hierarchical relationships and makes data organization explicit.
        """
        # Create the full prompt structure
        prompt_data = {
            "task": test_case.task,
            "data": test_case.data,
            "instructions": "Please analyze this information and provide a detailed response.",
        }

        return llml(prompt_data)


class ABTestRunner:
    """
    Orchestrates A/B testing of structured vs unstructured prompt formats.

    This class manages the comparison between VibeXML (structured) and raw text
    (unstructured) prompt formatting approaches for the same underlying data.
    """

    def __init__(self, ai_provider: PydanticAIProvider):
        """
        Initialize the A/B test runner.

        Args:
            ai_provider: The AI provider to use for generating responses
        """
        self.ai_provider = ai_provider

    async def run_single_test(self, test_case: StructuredTestCase) -> ABTestResult:
        """
        Run one test case with both formatting approaches.

        Args:
            test_case: The test case to evaluate

        Returns:
            Results containing both prompts and responses
        """
        # Generate both prompt formats
        raw_text_prompt = PromptFormatter.to_raw_text(test_case)
        vibexml_prompt = PromptFormatter.to_vibexml(test_case)

        print(f"  Testing: {test_case.name}")
        print(f"    Raw text prompt: {len(raw_text_prompt)} chars")
        print(f"    VibeXML prompt: {len(vibexml_prompt)} chars")

        # Get responses from AI for both formats
        print("    Generating raw text response...")
        raw_text_response = await self.ai_provider.generate_response(raw_text_prompt)

        print("    Generating VibeXML response...")
        vibexml_response = await self.ai_provider.generate_response(vibexml_prompt)

        return ABTestResult(
            test_case_name=test_case.name,
            raw_text_prompt=raw_text_prompt,
            vibexml_prompt=vibexml_prompt,
            raw_text_response=raw_text_response,
            vibexml_response=vibexml_response,
            raw_text_length=len(raw_text_prompt),
            vibexml_length=len(vibexml_prompt),
        )

    async def run_all_tests(
        self, test_cases: list[StructuredTestCase]
    ) -> list[ABTestResult]:
        """
        Run A/B tests on all provided test cases.

        Args:
            test_cases: List of test cases to evaluate

        Returns:
            List of results for all test cases
        """
        print(f"🔬 Running A/B Tests: Raw Text vs VibeXML")
        print(f"📊 {len(test_cases)} test cases")
        print(f"🤖 Using model: {self.ai_provider.model_name}")
        print()

        results = []
        for test_case in test_cases:
            result = await self.run_single_test(test_case)
            results.append(result)
            print()

        return results
