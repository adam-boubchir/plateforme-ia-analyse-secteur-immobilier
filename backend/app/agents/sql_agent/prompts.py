from app.agents.sql_agent.few_shot_provider import (
    FewShotProvider,
)


class PromptBuilder:
    """
    Build prompts for the SQL Agent.
    """

    SYSTEM_PROMPT = """
You are an expert Microsoft SQL Server assistant.

Your task is to generate a valid SQL Server query from a user's question.

Rules:

1. Return ONLY SQL.
2. Never explain your answer.
3. Never use Markdown.
4. Never use ```sql.
5. Use ONLY tables and columns provided in the database context.
6. Never invent table names or column names.
7. Use Microsoft SQL Server syntax.
8. Generate ONLY SELECT statements.
9. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE or EXEC statements.
10. Use JOINs whenever information is distributed across multiple tables.
11. Always use meaningful aliases.
12. If aggregation is used, always GROUP BY correctly.
13. If the question cannot be answered from the database context, return exactly:

CANNOT_GENERATE_SQL
"""

    def __init__(self):

        self.few_shot_provider = FewShotProvider()

    def build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the complete prompt sent to the LLM.
        """

        examples = self.few_shot_provider.get_examples(
            question
        )

        prompt = f"""
{self.SYSTEM_PROMPT}

DATABASE CONTEXT

{context}

================================================================================

EXAMPLES

{examples}

================================================================================

USER QUESTION

{question}

SQL:
"""

        return prompt.strip()