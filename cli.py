"""
Command line interface for interacting with the AI agent API.
"""

import httpx
import sys
import argparse
from typing import Optional


API_BASE_URL = "http://localhost:8000"


def check_health() -> bool:
    """Check if the API server is running."""
    try:
        response = httpx.get(f"{API_BASE_URL}/health", timeout=5.0)
        return response.status_code == 200
    except Exception:
        return False


def send_message(message: str, system_prompt: Optional[str] = None) -> str:
    """
    Send a message to the agent API and return the response.

    Args:
        message: The user's message
        system_prompt: Optional system prompt

    Returns:
        The agent's response
    """
    try:
        payload = {"message": message}
        if system_prompt:
            payload["system_prompt"] = system_prompt

        response = httpx.post(f"{API_BASE_URL}/chat", json=payload, timeout=30.0)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "No response received")
    except httpx.HTTPStatusError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        return f"Request Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def interactive_mode():
    """Run the CLI in interactive mode."""
    print("AI Agent CLI - Interactive Mode")
    print("=" * 50)
    print("Type your messages and press Enter. Type 'exit' or 'quit' to exit.")
    print("Type 'system: <prompt>' to set a system prompt for the next message.")
    print("=" * 50)
    print()

    if not check_health():
        print("Error: API server is not running. Please start the server first.")
        print(f"Run: python api.py or uvicorn api:app --reload")
        sys.exit(1)

    system_prompt = None

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if user_input.startswith("system:"):
                system_prompt = user_input[7:].strip()
                print(f"System prompt set: {system_prompt}")
                continue

            if user_input.lower() == "clear system":
                system_prompt = None
                print("System prompt cleared.")
                continue

            print("Agent: ", end="", flush=True)
            response = send_message(user_input, system_prompt)
            print(response)

            # Clear system prompt after first use
            if system_prompt:
                system_prompt = None

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


def single_message_mode(message: str, system_prompt: Optional[str] = None):
    """Send a single message and print the response."""
    if not check_health():
        print("Error: API server is not running. Please start the server first.")
        print(f"Run: python api.py or uvicorn api:app --reload")
        sys.exit(1)

    response = send_message(message, system_prompt)
    print(response)


def main():
    """Main CLI entry point."""
    global API_BASE_URL

    parser = argparse.ArgumentParser(description="CLI interface for the AI Agent API")
    parser.add_argument(
        "-m", "--message", type=str, help="Send a single message (non-interactive mode)"
    )
    parser.add_argument(
        "-s", "--system-prompt", type=str, help="System prompt to use with the message"
    )
    parser.add_argument(
        "--url",
        type=str,
        default=API_BASE_URL,
        help=f"API base URL (default: {API_BASE_URL})",
    )

    args = parser.parse_args()

    # Update API URL if provided
    if args.url:
        API_BASE_URL = args.url

    if args.message:
        single_message_mode(args.message, args.system_prompt)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
