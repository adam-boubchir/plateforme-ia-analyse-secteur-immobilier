from app.services.llm_service import LLMService


class SQLGenerator:
    """
    Generate SQL from a prepared prompt.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ):

        self.llm_service = llm_service

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate SQL from a prompt.
        """

        sql = self.llm_service.generate(
            agent_name="sql_agent",
            prompt=prompt,
        )

        print("\n" + "=" * 80)
        print("RAW GPT RESPONSE")
        print("=" * 80)
        print(sql)
        print("=" * 80 + "\n")

        return sql.strip()