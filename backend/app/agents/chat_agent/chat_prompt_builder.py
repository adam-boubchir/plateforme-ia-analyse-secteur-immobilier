from __future__ import annotations

from app.agents.chat_agent.chat_prompt import CHAT_SYSTEM_PROMPT

__all__ = ["ChatPromptBuilder"]


class ChatPromptBuilder:
    """
    Build the prompt sent to the Chat Agent.
    """

    USER_REQUEST_HEADER = "# USER REQUEST"

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build_prompt(
        self,
        question: str,
    ) -> str:
        """
        Build the complete prompt for the Chat Agent.

        Args:
            question: User natural language question.

        Returns:
            Fully formatted prompt.
        """

        return f"""
{CHAT_SYSTEM_PROMPT}

{self.USER_REQUEST_HEADER}

{question}
""".strip()