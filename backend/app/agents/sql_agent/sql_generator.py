from __future__ import annotations

import re

from app.services.llm_service import LLMService

__all__ = ["SQLGenerator"]


CANNOT_GENERATE_SQL = "CANNOT_GENERATE_SQL"

MARKDOWN_SQL_REGEX = r"```sql"

SQL_REGEX = r"(SELECT|WITH)\b.*"

SQL_PREFIXES = (
    "SQL:",
    "Sql:",
    "sql:",
)

AGENT_NAME = "sql_agent"


class SQLGenerator:
    """
    Generate a SQL query from the LLM response.

    Responsibilities
    ----------------
    - Send the prompt to the LLM.
    - Extract the SQL statement from the response.
    - Remove Markdown and formatting artifacts.
    - Return a normalized SQL query.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:

        self.llm_service = llm_service

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a SQL query from the given prompt.
        """

        response = self.llm_service.generate(
            agent_name=AGENT_NAME,
            prompt=prompt,
        )

        self._display_raw_response(
            response,
        )

        return self._extract_sql(
            response,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _extract_sql(
        self,
        response: str | None,
    ) -> str:
        """
        Extract and normalize the SQL statement returned by the LLM.
        """

        if not response:
            return ""

        response = response.strip()

        if response.upper() == CANNOT_GENERATE_SQL:
            return CANNOT_GENERATE_SQL

        response = self._remove_markdown(
            response,
        )

        response = self._remove_prefixes(
            response,
        )

        response = self._extract_statement(
            response,
        )

        return self._normalize_sql(
            response,
        )

    def _remove_markdown(
        self,
        response: str,
    ) -> str:
        """
        Remove Markdown code fences.
        """

        response = re.sub(
            MARKDOWN_SQL_REGEX,
            "",
            response,
            flags=re.IGNORECASE,
        )

        return response.replace(
            "```",
            "",
        ).strip()

    def _remove_prefixes(
        self,
        response: str,
    ) -> str:
        """
        Remove common SQL prefixes.
        """

        for prefix in SQL_PREFIXES:

            if response.startswith(prefix):

                return response[len(prefix):].strip()

        return response

    def _extract_statement(
        self,
        response: str,
    ) -> str:
        """
        Extract the SQL statement from the LLM response.
        """

        match = re.search(
            SQL_REGEX,
            response,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if match:

            return match.group(0)

        return response

    def _normalize_sql(
        self,
        sql: str,
    ) -> str:
        """
        Normalize the SQL statement.
        """

        sql = sql.strip()

        if sql.endswith(";"):

            sql = sql[:-1]

        return sql.strip()

    def _display_raw_response(
        self,
        response: str,
    ) -> None:
        """
        Display the raw LLM response for debugging purposes.
        """

        print()
        print("=" * 100)
        print("RAW LLM RESPONSE")
        print("=" * 100)
        print(response)
        print("=" * 100)
        print()