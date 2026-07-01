from app.dependencies.database import (
    get_ministry_session,
)

from app.dependencies.sql_agent import (
    get_sql_agent,
)


def main():

    print("=" * 80)
    print("SQL AGENT DEPENDENCY TEST")
    print("=" * 80)

    db = get_ministry_session()

    agent = get_sql_agent(db)

    print()

    print(
        "SQLAgent :",
        type(agent).__name__,
    )

    db.close()

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()