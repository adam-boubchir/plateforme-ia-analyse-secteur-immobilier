from abc import (
    ABC,
    abstractmethod,
)

from app.models.agent_models import (
    ModelConfig,
)


class BaseProvider(ABC):
    """
    Base interface for every LLM provider.

    Every provider (Azure OpenAI, OpenAI, Ollama,
    Gemini, Claude, etc.) must inherit from this class.

    Responsibilities
    ----------------
    • Validate the configuration
    • Receive a prompt
    • Call the LLM
    • Return the generated response
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    @abstractmethod
    def generate(
        self,
        config: ModelConfig,
        prompt: str,
    ) -> str:
        """
        Generate a response using the provider.
        """
        raise NotImplementedError

    # ==========================================================
    # OPTIONAL HOOKS
    # ==========================================================

    def validate_config(
        self,
        config: ModelConfig,
    ) -> None:
        """
        Validate the provider configuration.

        Providers may override this method if they require
        additional validation.
        """
        ...

    def before_generate(
        self,
        config: ModelConfig,
        prompt: str,
    ) -> None:
        """
        Hook executed immediately before sending
        the request to the LLM.
        """
        ...

    def after_generate(
        self,
        response: str,
    ) -> str:
        """
        Hook executed after receiving the response.

        The default implementation removes leading
        and trailing whitespace.
        """

        return response.strip()