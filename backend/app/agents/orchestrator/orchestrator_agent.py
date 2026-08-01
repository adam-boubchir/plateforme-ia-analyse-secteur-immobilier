from __future__ import annotations

from app.agents.orchestrator.orchestrator_generator import OrchestratorGenerator
from app.agents.orchestrator.orchestrator_prompt_builder import (
    OrchestratorPromptBuilder,
)
from app.agents.orchestrator.orchestrator_schema import OrchestratorDecision

__all__ = ["OrchestratorAgent"]


class OrchestratorAgent:
    """
    AI Orchestrator responsible for routing user requests
    to the appropriate AI agent.

    Pipeline:
        User Question
            ↓
        Prompt Builder
            ↓
        LLM Generation
            ↓
        Orchestrator Decision
    """

    def __init__(
        self,
        prompt_builder: OrchestratorPromptBuilder,
        generator: OrchestratorGenerator,
    ) -> None:
        self.prompt_builder = prompt_builder
        self.generator = generator

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def route(
        self,
        question: str,
    ) -> OrchestratorDecision:
        """
        Determine which AI agent should process the user's request.

        Args:
            question: User natural language question.

        Returns:
            OrchestratorDecision describing the selected agent.
        """

        prompt = self.prompt_builder.build_prompt(
            question=question,
        )

        return self.generator.generate(
            prompt=prompt,
        )