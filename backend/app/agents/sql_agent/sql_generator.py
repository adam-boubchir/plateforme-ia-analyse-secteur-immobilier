import re

from app.services.llm_service import (
    LLMService,
)


class SQLGenerator:
    """
    Responsible for generating SQL from the LLM.

    This class acts as a bridge between the SQL Agent
    and the LLM.

    Responsibilities
    ----------------
    • Send the prompt
    • Retrieve the response
    • Clean the response
    • Extract the SQL query
    """

    def __init__(
        self,
        llm_service: LLMService,
    ):

        self.llm_service = llm_service

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate SQL from the prompt.
        """

        response = self.llm_service.generate(

            agent_name="sql_agent",

            prompt=prompt,

        )

        self._print_raw_response(
            response
        )

        sql = self._extract_sql(
            response
        )

        return sql

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _extract_sql(
        self,
        response: str,
    ) -> str:
        """
        Clean the LLM response and extract SQL.
        """

        if response is None:

            return ""

        response = response.strip()

        if response == "":

            return ""

        # ------------------------------------------------------
        # Impossible question
        # ------------------------------------------------------

        if response.upper() == "CANNOT_GENERATE_SQL":

            return "CANNOT_GENERATE_SQL"

        # ------------------------------------------------------
        # Remove Markdown
        # ------------------------------------------------------

        response = re.sub(

            r"```sql",

            "",

            response,

            flags=re.IGNORECASE,

        )

        response = response.replace(
            "```",
            "",
        )

        response = response.strip()

        # ------------------------------------------------------
        # Remove useless prefixes
        # ------------------------------------------------------

        prefixes = [

            "SQL:",

            "Sql:",

            "sql:",

        ]

        for prefix in prefixes:

            if response.startswith(prefix):

                response = response[
                    len(prefix):
                ].strip()

        # ------------------------------------------------------
        # Keep only SQL
        # ------------------------------------------------------

        match = re.search(

            r"(SELECT|WITH)\b.*",

            response,

            flags=re.IGNORECASE | re.DOTALL,

        )

        if match:

            response = match.group(0)

        response = response.strip()

        if response.endswith(";"):

            response = response[:-1].strip()

        return response

    def _print_raw_response(
        self,
        response: str,
    ) -> None:
        """
        Print raw LLM output.
        """

        print()

        print("=" * 100)

        print("RAW LLM RESPONSE")

        print("=" * 100)

        print(response)

        print("=" * 100)

        print()