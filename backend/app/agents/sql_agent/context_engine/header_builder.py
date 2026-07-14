class HeaderBuilder:
    """
    Build the header of the SQL context.
    """

    def build(self) -> list[str]:
        """
        Build the header section.
        """

        return [

            "=" * 100,

            "DATABASE CONTEXT",

            "=" * 100,

            "",

            "DATABASE",

            "Name : OBSERVATOIRE_STAGIAIRE",

            "Purpose : Moroccan Real Estate Observatory",

            "Language : French",

            "Currency : MAD",

            "",

            "=" * 100,

            "",

        ]