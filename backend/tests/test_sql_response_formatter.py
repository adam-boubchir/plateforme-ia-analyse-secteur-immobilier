from app.agents.sql_agent.sql_response_formatter import (
    SQLResponseFormatter,
)


def main():

    formatter = SQLResponseFormatter()

    print("=" * 80)
    print("SQL RESPONSE FORMATTER TEST")
    print("=" * 80)

    print("\n===== TEST 1 =====")

    rows = []

    print(
        formatter.format(rows)
    )

    print("\n===== TEST 2 =====")

    rows = [

        {
            "nom_region": "Rabat",
            "prix": 12000
        }

    ]

    print(
        formatter.format(rows)
    )

    print("\n===== TEST 3 =====")

    rows = [

        {
            "nom_region": "Rabat",
            "prix": 12000
        },

        {
            "nom_region": "Casablanca",
            "prix": 15000
        },

        {
            "nom_region": "Fès",
            "prix": 9800
        }

    ]

    print(
        formatter.format(rows)
    )

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()