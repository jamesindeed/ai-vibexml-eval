"""
AI Provider Interface using Pydantic AI

This module provides a clean interface to LLM providers using Pydantic AI
with OpenRouter for maximum model flexibility.
"""

import os
from typing import Optional, Type, TypeVar

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

T = TypeVar("T", bound=BaseModel)


class PydanticAIProvider:
    """
    Pydantic AI provider using OpenRouter for research-grade LLM evaluation.

    This provider supports any model available through OpenRouter, enabling
    easy comparison across different model families and providers.
    """

    def __init__(
        self,
        model: str = "anthropic/claude-3.5-sonnet",
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize the Pydantic AI provider.

        Args:
            model: OpenRouter model identifier (e.g., "anthropic/claude-3.5-sonnet")
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            system_prompt: Custom system prompt (uses default if None)
        """
        self.model_name = model

        # Create the OpenRouter provider
        provider = OpenRouterProvider(
            api_key=api_key or os.getenv("OPENROUTER_API_KEY")
        )

        # Create the model
        self.model = OpenAIModel(model, provider=provider)

        # Default system prompt for evaluation tasks
        default_system_prompt = (
            "You are an expert AI assistant designed for research evaluation. "
            "Follow instructions precisely and provide detailed, accurate responses. "
            "When analyzing structured data, pay careful attention to hierarchical "
            "relationships, dependencies, and organizational patterns."
        )

        # Store the system prompt for reuse
        self.system_prompt = system_prompt or default_system_prompt

        # Create the agent
        self.agent = Agent(
            self.model,
            system_prompt=self.system_prompt,
        )

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response to the given prompt.

        Args:
            prompt: The input prompt

        Returns:
            The generated response text

        Raises:
            Exception: If response generation fails
        """
        try:
            result = await self.agent.run(prompt)
            return result.data
        except Exception as e:
            raise Exception(f"Response generation failed: {str(e)}")

    async def generate_structured_response(
        self, prompt: str, response_model: Type[T]
    ) -> T:
        """
        Generate a structured response using a Pydantic model.

        This ensures the response conforms exactly to the specified structure
        and is automatically validated and parsed.

        Args:
            prompt: The input prompt
            response_model: Pydantic model class defining the expected response structure

        Returns:
            Validated and parsed response as the specified Pydantic model

        Raises:
            Exception: If response generation fails
        """
        try:
            # Create a new agent with the response model
            structured_agent = Agent(
                self.model, result_type=response_model, system_prompt=self.system_prompt
            )

            result = await structured_agent.run(prompt)
            return result.data
        except Exception as e:
            raise Exception(f"Structured response generation failed: {str(e)}")

    def __repr__(self) -> str:
        return f"PydanticAIProvider(model='{self.model_name}')"
