from app.database.session import get_immo_db

from app.services.metadata_service import MetadataService

from app.agents.sql_agent.sql_context_builder import (
    SQLContextBuilder,
)

from app.agents.sql_agent.prompts import PromptBuilder


def main():

    db = next(get_immo_db())

    try:

        print("=" * 80)
        print("PROMPT BUILDER TEST")
        print("=" * 80)

        # Metadata service
        metadata_service = MetadataService(db)

        # Build database context
        context_builder = SQLContextBuilder(
            metadata_service
        )

        context = context_builder.build_context()

        # User question
        question = (
            "Quel est le prix moyen des appartements à Rabat ?"
        )

        # Build prompt
        prompt_builder = PromptBuilder()

        prompt = prompt_builder.build_prompt(
            question=question,
            context=context,
        )

        print("\nGENERATED PROMPT\n")
        print("=" * 80)
        print(prompt)
        print("=" * 80)

        print(f"\nPrompt length : {len(prompt)} characters")

        print("\n✅ TEST PASSED")

    finally:

        db.close()


if __name__ == "__main__":
    main()