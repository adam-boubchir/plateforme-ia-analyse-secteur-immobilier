from app.services.llm_service import LLMService


class SQLGenerator:

    def __init__(self):

        self.llm = LLMService()

    def generate_sql(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = f"""
You are an expert SQL Server assistant.

Generate ONLY one SQL query.

Rules:

- SQL Server syntax only.
- Return ONLY SQL.
- No explanation.
- No markdown.
- Only SELECT queries.
- Never generate INSERT.
- Never generate UPDATE.
- Never generate DELETE.
- Never generate DROP.
- Never generate ALTER.

Database schema_name:

{context}

User question:

{question}
"""

        return self.llm.generate(prompt)