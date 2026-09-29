from __future__ import annotations

from app.agents.prediction_agent.prediction_agent import (
    PredictionAgent,
)

from app.models.agent_response import (
    AgentResponse,
)


# ==========================================================
# FAKE SQL AGENT
# ==========================================================

class FakeSQLAgent:
    """
    Fake SQL Agent used to simulate the retrieval
    of historical data from the database.
    """

    def ask(
        self,
        *,
        question: str,
        conversation_id: int,
    ) -> AgentResponse:

        print()
        print("=" * 60)
        print("FAKE SQL AGENT")
        print("=" * 60)

        print(f"Question: {question}")
        print(f"Conversation ID: {conversation_id}")

        rows = [

            {
                "year": 2018,
                "value": 100,
            },

            {
                "year": 2019,
                "value": 115,
            },

            {
                "year": 2020,
                "value": 130,
            },

            {
                "year": 2021,
                "value": 145,
            },

            {
                "year": 2022,
                "value": 160,
            },

            {
                "year": 2023,
                "value": 180,
            },

            {
                "year": 2024,
                "value": 200,
            },

        ]

        return AgentResponse(

            success=True,

            error=None,

            answer=(
                "Données historiques récupérées "
                "avec succès."
            ),

            sql="""
SELECT
    year,
    value
FROM historical_data
ORDER BY year
""".strip(),

            rows=rows,

            data={},

        )


# ==========================================================
# MAIN TEST
# ==========================================================

def main() -> None:

    print()
    print("=" * 70)
    print("PREDICTION AGENT INTEGRATION TEST")
    print("=" * 70)

    # ======================================================
    # FAKE SQL AGENT
    # ======================================================

    sql_agent = FakeSQLAgent()

    # ======================================================
    # PREDICTION AGENT
    # ======================================================

    prediction_agent = PredictionAgent(

        sql_agent=sql_agent,

    )

    # ======================================================
    # QUESTION
    # ======================================================

    question = (
        "Prédit la valeur pour les 3 prochaines années."
    )

    # ======================================================
    # EXECUTE
    # ======================================================

    response = prediction_agent.ask(

        question=question,

        conversation_id=1,

    )

    # ======================================================
    # RESULT
    # ======================================================

    print()
    print("=" * 70)
    print("FINAL RESPONSE")
    print("=" * 70)

    print()

    print("Success:")
    print(response.success)

    print()

    print("Answer:")
    print(response.answer)

    print()

    print("SQL:")
    print(response.sql)

    print()

    print("Rows:")
    print(response.rows)

    print()

    print("Data:")
    print(response.data)

    print()

    print("=" * 70)

    if response.success:

        print("TEST PASSED")

    else:

        print("TEST FAILED")
        print(response.error)

    print("=" * 70)
    print()


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()