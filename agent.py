"""
Basic AI Agent module for call/response functionality.
"""

from typing import Optional
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class Agent:
    """Basic AI agent that handles call/response interactions."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize the agent.

        Args:
            model: The OpenAI model to use (default: gpt-3.5-turbo)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def call(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Process a message and return a response.

        Args:
            message: The user's message/query
            system_prompt: Optional system prompt to guide the agent's behavior

        Returns:
            The agent's response as a string
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
