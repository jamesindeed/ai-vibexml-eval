# LLML Evaluation Framework

An evaluation system for comparing structured (VibeXML) vs unstructured (raw text) data formatting in AI prompts, using LLM-as-a-judge methodology.

## Overview

This framework provides a comprehensive, paper-worthy evaluation of whether structured data formatting (using LLML's VibeXML approach) provides measurable advantages over traditional unstructured text formatting for AI prompt engineering.

### Key Features

- **Research-Grade Methodology**: Uses LLM-as-a-judge for objective evaluation
- **Comprehensive Test Cases**: Carefully designed scenarios where structure should matter
- **Model Agnostic**: Works with any model available through OpenRouter
- **Detailed Analysis**: Multi-criteria scoring with statistical analysis
- **Reproducible Results**: Saves complete evaluation data for peer review

## Architecture

```
vibexml_evaluation/
├── __init__.py           # Package initialization
├── providers.py          # Pydantic AI provider interface
├── test_cases.py         # Curated test case dataset
├── runner.py            # A/B test orchestration
├── judge.py             # LLM-based evaluation
├── evaluator.py         # Main evaluation orchestrator
├── run_evaluation.py    # Command-line interface
└── README.md            # This documentation
```

## Installation

1. **Install Dependencies**:
   ```bash
   pip install pydantic-ai-slim[openai]
   ```

2. **Set API Key**:
   ```bash
   export OPENROUTER_API_KEY="your-openrouter-api-key"
   ```
   Get your API key from: https://openrouter.ai/keys

3. **Verify Installation**:
   ```bash
   vibexml-eval --list-models
   ```

## Quick Start

### Basic Evaluation
```bash
# Run complete evaluation with default models
python run_evaluation.py

# Use specific models (recommended for research)
python run_evaluation.py --model anthropic/claude-3.5-sonnet --judge openai/gpt-4o
```

### Development Testing
```bash
# Quick test with fewer cases
python run_evaluation.py --model anthropic/claude-3.5-haiku --cases 2

# Debug single test case
python run_evaluation.py --single nested_conditional_logic

# Reproducible evaluation with fixed random seed
python run_evaluation.py --model anthropic/claude-3.5-sonnet --seed 42
```

### Information Commands
```bash
# List available test cases
python run_evaluation.py --list-cases

# Show recommended models
python run_evaluation.py --list-models
```

## Test Cases

The framework includes 5 carefully designed test cases where structured formatting should provide measurable advantages:

1. **Nested Conditional Logic**: Complex deployment decisions with approval matrices
2. **Workflow Dependencies**: CI/CD pipelines with conditional execution
3. **Hierarchical Analysis**: Organizational data requiring structural understanding
4. **Configuration Parsing**: Complex nested configurations with interdependencies
5. **Multi-Context Decisions**: Incident response across multiple system contexts

Each test case includes:
- Structured data representing realistic scenarios
- Clear tasks requiring hierarchical understanding
- Expected advantages that structured formatting should provide
- Evaluation criteria specific to the scenario

## Evaluation Methodology

### 1. Response Generation
- Each test case is formatted in two ways:
  - **Unstructured**: Traditional string concatenation
  - **Structured**: VibeXML markup using LLML
- AI generates responses to both formats

### 2. LLM-as-Judge Evaluation
- Independent LLM evaluates both responses **blindly** (randomized A/B order)
- Multi-criteria scoring (0-100 scale):
  - Accuracy & Completeness
  - Structured Data Utilization
  - Precision & Specificity
  - Logical Flow & Organization
  - Contextual Understanding

### 3. Statistical Analysis
- Win/loss rates across all test cases
- Average score differences
- Criteria-specific advantages
- Confidence intervals and significance testing

## Recommended Model Combinations

### For Research Papers
```bash
# Different model families (reduces bias)
--model anthropic/claude-3.5-sonnet --judge openai/gpt-4o
--model openai/gpt-4o --judge anthropic/claude-3.5-sonnet
```

### For Development
```bash
# Fast, cost-effective
--model anthropic/claude-3.5-haiku
```

### For Maximum Capability
```bash
# Latest high-capability models
--model anthropic/claude-4-sonnet-20250514 --judge openai/gpt-4o
```

## Output Format

Results are saved as comprehensive JSON files containing:

```json
{
  "metadata": {
    "test_type": "llml_structured_vs_unstructured",
    "response_model": "anthropic/claude-3.5-sonnet",
    "judge_model": "openai/gpt-4o",
    "evaluation_timestamp": "2024-01-15T14:30:00Z"
  },
  "ab_test_results": [
    {
      "test_case_name": "nested_conditional_logic",
      "raw_text_prompt": "...",
      "vibexml_prompt": "...",
      "raw_text_response": "...",
      "vibexml_response": "...",
      "raw_text_length": 1234,
      "vibexml_length": 1456
    }
  ],
  "judgments": [
    {
      "test_case_name": "nested_conditional_logic",
      "winner": "vibexml",
      "confidence": 85,
      "raw_text_score": 76.4,
      "vibexml_score": 88.4,
      "reasoning": "Response B demonstrates significantly better...",
      "criteria_scores": {
        "accuracy_completeness": {"raw_text": 78, "vibexml": 89},
        "structured_data_utilization": {"raw_text": 70, "vibexml": 92}
      }
    }
  ],
  "analysis": {
    "summary": {
      "total_tests": 5,
      "vibexml_wins": 4,
      "vibexml_win_rate": 80.0
    },
    "average_scores": {
      "vibexml_advantage": 12.3
    }
  }
}
```

### Adding New Test Cases
```python
@classmethod
def your_custom_test(cls) -> StructuredTestCase:
    return StructuredTestCase(
        name="your_test_name",
        description="Your scenario description",
        data={"your": "structured_data"},
        task="Your specific task",
        why_structure_helps="Why structure should help here",
        expected_advantages=["advantage1", "advantage2"]
    )
```

### Custom Evaluation Criteria
Modify the judge prompt in `judge.py` to include domain-specific criteria.

### Alternative Formatting
Replace the VibeXML formatter in `runner.py` with your preferred structured format.

### Bias Prevention
- **Blind Evaluation**: Response order is randomized (A/B) to prevent judge bias
- **Reproducible Results**: Optional `--seed` parameter for deterministic randomization
- **Cross-Model Validation**: Use different models for generation vs judging

### Limitations & Future Work
- Prompt length differences between formats need controlled comparison (May be redundant since it doesn't add more context, just structure with tags <xml></xml>)
- Test case selection bias requires neutral/adversarial case additions
- Human validation recommended for publication-quality results
