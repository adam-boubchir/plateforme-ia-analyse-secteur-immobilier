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
10. If the question cannot be answered from the database context, return exactly:

CANNOT_GENERATE_SQL
"""

    def build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the complete prompt sent to the LLM.
        """

        prompt = f"""
{self.SYSTEM_PROMPT}

DATABASE CONTEXT

{context}

USER QUESTION

{question}

SQL:
"""

        return prompt.strip()