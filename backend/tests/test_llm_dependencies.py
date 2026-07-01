from app.dependencies.database import (
    get_immo_session,
)

from app.dependencies.llm import (
    get_model_manager,
    get_llm_service,
    get_sql_generator,
)


def main():

    print("=" * 80)
    print("LLM DEPENDENCIES TEST")
    print("=" * 80)

    db = get_immo_session()

    model_manager = get_model_manager(db)

    llm_service = get_llm_service(db)

    sql_generator = get_sql_generator(db)

    print()

    print(
        "ModelManager :",
        type(model_manager).__name__,
    )

    print(
        "LLMService :",
        type(llm_service).__name__,
    )

    print(
        "SQLGenerator :",
        type(sql_generator).__name__,
    )

    db.close()

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()