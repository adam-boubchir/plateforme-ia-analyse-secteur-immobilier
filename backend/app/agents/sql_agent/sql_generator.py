from __future__ import annotations

import re

from app.services.llm_service import LLMService

__all__ = ("SQLGenerator",)

# ==========================================================
# CONSTANTS
# ==========================================================

_CANNOT_GENERATE_SQL = "CANNOT_GENERATE_SQL"

_MARKDOWN_SQL_REGEX = r"```sql"
_SQL_REGEX = r"(SELECT|WITH)\b.*"

_SQL_PREFIXES = (
    "SQL:",
    "Sql:",
    "sql:",
)

_AGENT_NAME = "sql_agent"


class SQLGenerator:
    """
    Generate a SQL query from a Large Language Model.

    Responsibilities
    ----------------
    - Send the prompt to the LLM.
    - Extract the SQL statement.
    - Remove formatting artifacts.
    - Return a normalized SQL query.
    """

    def __init__(
        self,
        *,
        llm_service: LLMService,
    ) -> None:
        self._llm_service = llm_service

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        *,
        prompt: str,
    ) -> str:
        """
        Generate a SQL query from a prompt.

        Args:
            prompt:
                Prompt sent to the language model.

        Returns:
            Normalized SQL query.
        """

        response = self._llm_service.generate(
            agent_name=_AGENT_NAME,
            prompt=prompt,
        )

        self._display_raw_response(
            response=response,
        )

        sql = self._extract_sql(
            response=response,
        )

        return sql

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _extract_sql(
        self,
        *,
        response: str | None,
    ) -> str:
        """
        Extract and normalize the SQL query returned by the LLM.

        Args:
            response:
                Raw LLM response.

        Returns:
            Normalized SQL query.
        """

        if not response:
            return ""

        cleaned_response = response.strip()

        if cleaned_response.upper() == _CANNOT_GENERATE_SQL:
            return _CANNOT_GENERATE_SQL

        cleaned_response = self._remove_markdown(
            response=cleaned_response,
        )

        cleaned_response = self._remove_prefixes(
            response=cleaned_response,
        )

        cleaned_response = self._extract_statement(
            response=cleaned_response,
        )

        normalized_sql = self._normalize_sql(
            sql=cleaned_response,
        )

        return normalized_sql

    @staticmethod
    def _remove_markdown(
        *,
        response: str,
    ) -> str:
        """
        Remove Markdown code fences.
        """

        cleaned_response = re.sub(
            _MARKDOWN_SQL_REGEX,
            "",
            response,
            flags=re.IGNORECASE,
        )

        cleaned_response = cleaned_response.replace(
            "```",
            "",
        ).strip()

        return cleaned_response

    @staticmethod
    def _remove_prefixes(
        *,
        response: str,
    ) -> str:
        """
        Remove common SQL prefixes.
        """

        cleaned_response = response

        for prefix in _SQL_PREFIXES:
            if cleaned_response.startswith(prefix):
                cleaned_response = cleaned_response[
                    len(prefix):
                ].strip()
                break

        return cleaned_response

    @staticmethod
    def _extract_statement(
        *,
        response: str,
    ) -> str:
        """
        Extract the SQL statement from the LLM response.
        """

        match = re.search(
            _SQL_REGEX,
            response,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if match:
            sql = match.group(0)
        else:
            sql = response

        return sql

    @staticmethod
    def _normalize_sql(
        *,
        sql: str,
    ) -> str:
        """
        Normalize a SQL query.
        """

        normalized_sql = sql.strip()

        if normalized_sql.endswith(";"):
            normalized_sql = normalized_sql[:-1]

        normalized_sql = normalized_sql.strip()

        return normalized_sql

    @staticmethod
    def _display_raw_response(
        *,
        response: str,
    ) -> None:
        """
        Display the raw LLM response.

        This method is intended for debugging and can later be
        replaced by the application logger.
        """

        print()
        print("=" * 100)
        print("RAW LLM RESPONSE")
        print("=" * 100)
        print(response)
        print("=" * 100)
        print()