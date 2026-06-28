from app.agents.sql_agent.sql_validator import (
    SQLValidator,
    SQLValidationError,
)


def run_test(sql: str):

    validator = SQLValidator()

    print("=" * 80)
    print(sql)
    print("-" * 80)

    try:

        result = validator.validate(sql)

        print("✅ VALID")
        print(result)

    except SQLValidationError as e:

        print("❌ INVALID")
        print(e)


def main():

    print("=" * 80)
    print("SQL VALIDATOR TEST")
    print("=" * 80)

    test_queries = [

        # Valid query
        """
        SELECT *
        FROM REGION
        """,

        # DELETE
        """
        DELETE FROM REGION
        """,

        # UPDATE
        """
        UPDATE REGION
        SET nom_region='Test'
        """,

        # DROP
        """
        DROP TABLE REGION
        """,

        # Multiple statements
        """
        SELECT *
        FROM REGION;

        DROP TABLE REGION
        """,

        # Empty
        "",

        # LLM failed
        "CANNOT_GENERATE_SQL",

        # No FROM
        """
        SELECT 1
        """,

    ]

    for query in test_queries:

        run_test(query)


if __name__ == "__main__":
    main()