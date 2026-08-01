from __future__ import annotations

from app.agents.orchestrator.orchestrator_prompt import (
    ORCHESTRATOR_SYSTEM_PROMPT,
)

__all__ = ["OrchestratorPromptBuilder"]

# ==========================================================
# CONSTANTS
# ==========================================================

USER_REQUEST_TITLE = "USER REQUEST"


class OrchestratorPromptBuilder:
    """
    Build the prompt sent to the Orchestrator LLM.

    Responsibilities:
        - Inject the system prompt.
        - Inject the user request.
        - Return the complete prompt.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build_prompt(
        self,
        question: str,
    ) -> str:
        """
        Build the complete orchestrator prompt.

        Args:
            question: User natural language question.

        Returns:
            Fully formatted prompt.
        """

        return "\n\n".join(
            (
                ORCHESTRATOR_SYSTEM_PROMPT,
                self._section(
                    USER_REQUEST_TITLE,
                    question,
                ),
            )
        ).strip()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _section(
        self,
        title: str,
        body: str,
    ) -> str:
        """
        Build a formatted prompt section.

        Args:
            title: Section title.
            body: Section content.

        Returns:
            Formatted markdown section.
        """

        return f"# {title}\n\n{body}"