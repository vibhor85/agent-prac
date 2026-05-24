import os
from typing import Any

from groq import Groq
from debug import log

from tools import TOOLS


class ChatClient:
    """Manages Groq chat interactions with message history."""

    def __init__(self, system_prompt: str):
        """Initialize the client with a system prompt."""
        self.system_prompt = system_prompt
        self.messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt}
        ]
        self.groq_client = self._create_client()
        log("[log] ChatClient initialized")

    def _create_client(self) -> Groq:
        """Create a Groq client using the API key from the environment."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in the environment.")

        log("[log] Creating Groq client")
        return Groq(api_key=api_key)

    def push_message(
        self,
        role: str,
        content: str,
        tool_call_id: str = None,
        name: str = None,
    ) -> None:

        # Tool response message
        if role == "tool":
            msg = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content,
            }

        # Normal message
        else:
            msg = {
                "role": role,
                "content": content,
            }

            if name:
                msg["name"] = name

        self.messages.append(msg)

        log(
            f"[log] Message pushed: role={role}, content_len={len(content or '')}"
        )

    def append_message(self, message: dict[str, Any]) -> None:
        """Append a raw message dict to the chat history."""
        self.messages.append(message)
        log(
            f"[log] Raw message appended: {message.get('role')} keys={list(message.keys())}")

    def get_messages(self) -> list[dict[str, str]]:
        """Return the current message history."""
        log(f"[log] Retrieving {len(self.messages)} messages")
        return self.messages.copy()

    def add_user_message(self, content: str) -> None:
        """Convenience method to add a user message."""
        self.push_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        """Convenience method to add an assistant message."""
        self.push_message("assistant", content)

    def create_chat_completion(self) -> Any:
        """Call the chat completions API with current message history.

        Args:
            model: Model name to use (default: llama-3.3-70b-versatile)

        Returns:
            Chat completion response from Groq API
        """

        model = os.getenv("MODEL_NAME")
        if not model:
            raise RuntimeError("MODEL_NAME is not set in the environment.")
        messages = self.get_messages()
        log(
            f"[log] Sending chat completion request with model={model} and tools={TOOLS}")

        try:
            return self.groq_client.chat.completions.create(messages=messages, model=model, tools=TOOLS, tool_choice="auto", temperature=0)
        except Exception as e:
            log("[error] chat completion request failed: " + str(e))
            log("[error] messages sent (repr): " + repr(messages))
            raise
