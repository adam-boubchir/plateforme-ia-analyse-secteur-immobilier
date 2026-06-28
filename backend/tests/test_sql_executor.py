from app.database.session import get_ministry_db

from app.agents.sql_agent.sql_executor import (
    SQLExecutor,
)


def main():

    db = next(
        get_ministry_db()
    )

    try:

        executor = SQLExecutor(db)

        sql = """
        SELECT TOP (5)

            id_region,

            nom_region

        FROM REGION

        ORDER BY id_region
        """

        result = executor.execute(sql)

        print("=" * 80)
        print("SQL EXECUTOR TEST")
        print("=" * 80)

        print()

        for row in result:

            print(row)

        print()

        print(
            f"Returned {len(result)} rows."
        )

        print()

        print("✅ TEST PASSED")

    finally:

        db.close()


if __name__ == "__main__":
    main()