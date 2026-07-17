import time

from sqlalchemy.orm import Session

from app.services.model_manager import (
    ModelManager,
)

from app.services.providers.provider_factory import (
    ProviderFactory,
)


class LLMService:
    """
    Central service responsible for interacting with
    Large Language Models.

    Responsibilities
    ----------------
    • Retrieve the model configuration
    • Instantiate the correct provider
    • Send prompts
    • Return generated responses
    • Measure execution time
    """

    def __init__(
        self,
        db: Session,
    ):

        self.model_manager = ModelManager(
            db
        )

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        agent_name: str,
        prompt: str,
    ) -> str:
        """
        Generate a response using the configured model.
        """

        config = self._load_configuration(
            agent_name
        )

        provider = ProviderFactory.create(
            config
        )

        start = time.perf_counter()

        response = provider.generate(

            config=config,

            prompt=prompt,

        )

        elapsed = (
            time.perf_counter() - start
        )

        self._print_debug(

            agent_name,

            config,

            elapsed,

        )

        return response.strip()

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _load_configuration(
        self,
        agent_name: str,
    ):
        """
        Load the model configuration.
        """

        config = self.model_manager.get(
            agent_name
        )

        if config is None:

            raise ValueError(

                f"No model configured for agent '{agent_name}'."

            )

        return config

    def _print_debug(
        self,
        agent_name: str,
        config,
        elapsed: float,
    ) -> None:
        """
        Display execution information.
        """

        print()

        print("=" * 100)

        print("LLM EXECUTION")

        print("=" * 100)

        print(
            f"Agent      : {agent_name}"
        )

        print(
            f"Provider   : {config.provider}"
        )

        print(
            f"Model      : {config.model_name}"
        )

        print(
            f"Deployment : {getattr(config, 'deployment_name', '-')}"
        )

        print(
            f"Execution  : {elapsed:.2f} sec"
        )

        print("=" * 100)

        print()