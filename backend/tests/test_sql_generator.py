from app.agents.sql_agent.sql_generator import SQLGenerator


class FakeLLMService:
    """
    Fake LLM used for unit testing.
    """

    def generate(
        self,
        agent_name: str,
        prompt: str,
    ) -> str:

        print("=" * 80)
        print("LLM CALLED")
        print("=" * 80)

        print(f"Agent : {agent_name}")

        print("\nPrompt received:\n")
        print(prompt)

        return """
SELECT TOP (5)
    nom_region
FROM REGION
ORDER BY nom_region
"""


def main():

    print("=" * 80)
    print("SQL GENERATOR TEST")
    print("=" * 80)

    generator = SQLGenerator(
        llm_service=FakeLLMService()
    )

    prompt = """
You are an SQL assistant.

Generate SQL.

Question:
List all regions.
"""

    sql = generator.generate(prompt)

    print("\nGenerated SQL\n")

    print(sql)

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()