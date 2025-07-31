"""
LLML Evaluation Framework

A comprehensive evaluation system for comparing structured (VibeXML) vs unstructured (raw text)
data formatting in AI prompts, using LLM-as-a-judge methodology.

This framework is designed for research-grade evaluation of prompt formatting strategies.
"""

__version__ = "1.0.0"

from .evaluator import LLMLEvaluator
from .providers import PydanticAIProvider
from .test_cases import StructuredTestCase, TestCaseDataset

__all__ = [
    "LLMLEvaluator",
    "PydanticAIProvider",
    "StructuredTestCase",
    "TestCaseDataset",
]
