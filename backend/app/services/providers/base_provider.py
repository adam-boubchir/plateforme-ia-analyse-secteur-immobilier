from abc import (
    ABC,
    abstractmethod,
)

from app.models.agent_models import (
    ModelConfig,
)


class BaseProvider(ABC):
    """
    Abstract base class for every LLM provider.

    Every provider (Azure OpenAI, OpenAI, Ollama, Gemini,
    Claude, etc.) must inherit from this class.

    Responsibilities
    ----------------
    • Receive a ModelConfig
    • Receive a prompt
    • Return the generated text
    """

    @abstractmethod
    def generate(
        self,
        config: ModelConfig,
        prompt: str,
    ) -> str:
        """
        Generate a response from the LLM.

        Parameters
        ----------
        config:
            Model configuration.

        prompt:
            Prompt sent to the model.

        Returns
        -------
        str
            Generated response.
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
        Optional configuration validation.

        Providers can override this method if they
        require additional checks.
        """

        pass

    def before_generate(
        self,
        config: ModelConfig,
        prompt: str,
    ) -> None:
        """
        Hook executed before sending the request.
        """

        pass

    def after_generate(
        self,
        response: str,
    ) -> str:
        """
        Hook executed after receiving the response.

        By default it simply strips whitespace.
        """

        return response.strip()