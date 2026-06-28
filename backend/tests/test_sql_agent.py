from app.agents.sql_agent.sql_agent import SQLAgent


class FakeContextBuilder:

    def build_context(self):

        print("✓ ContextBuilder called")

        return "DATABASE CONTEXT"


class FakePromptBuilder:

    def build_prompt(
        self,
        question: str,
        context: str,
    ):

        print("✓ PromptBuilder called")

        return f"""
Context:
{context}

Question:
{question}
"""


class FakeGenerator:

    def generate(
        self,
        prompt: str,
    ):

        print("✓ SQLGenerator called")

        return """
SELECT *
FROM REGION
"""


class FakeValidator:

    def validate(
        self,
        sql: str,
    ):

        print("✓ SQLValidator called")

        return sql


class FakeExecutor:

    def execute(
        self,
        sql: str,
    ):

        print("✓ SQLExecutor called")

        return [

            {
                "nom_region": "Rabat"
            },

            {
                "nom_region": "Casablanca"
            }

        ]


class FakeFormatter:

    def format(
        self,
        rows,
    ):

        print("✓ SQLResponseFormatter called")

        return "2 régions trouvées."


def main():

    print("=" * 80)
    print("SQL AGENT TEST")
    print("=" * 80)

    agent = SQLAgent(

        context_builder=FakeContextBuilder(),

        prompt_builder=FakePromptBuilder(),

        generator=FakeGenerator(),

        validator=FakeValidator(),

        executor=FakeExecutor(),

        formatter=FakeFormatter(),

    )

    response = agent.ask(

        "Liste des régions"

    )

    print()

    print("=" * 80)
    print("SQL AGENT RESPONSE")
    print("=" * 80)

    print(response.model_dump())

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()