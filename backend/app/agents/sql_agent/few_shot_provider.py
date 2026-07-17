from app.agents.sql_agent.few_shots.examples import (
    FEW_SHOT_EXAMPLES,
)


class FewShotProvider:
    """
    Provides the most relevant few-shot examples
    according to the detected user question.

    This class can later be replaced by a vector
    search (embeddings/RAG) without modifying the
    PromptBuilder.
    """

    def __init__(self):

        self.examples = FEW_SHOT_EXAMPLES

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def get_examples(
        self,
        question: str,
        max_examples: int = 3,
    ) -> str:
        """
        Return the most relevant examples.
        """

        ranked_examples = self._rank_examples(
            question
        )

        if not ranked_examples:

            return "No example available."

        prompt = []

        for example in ranked_examples[:max_examples]:

            prompt.extend(
                self._format_example(example)
            )

        return "\n".join(prompt)

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _rank_examples(
        self,
        question: str,
    ):
        """
        Very simple keyword ranking.

        This will later be replaced by
        semantic search.
        """

        question = question.lower()

        scored = []

        for example in self.examples:

            score = 0

            keywords = example.get(
                "keywords",
                [],
            )

            for keyword in keywords:

                if keyword.lower() in question:

                    score += 1

            scored.append(
                (
                    score,
                    example,
                )
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [

            example

            for score, example in scored

            if score > 0

        ]

    def _format_example(
        self,
        example: dict,
    ):

        lines = []

        lines.append("=" * 60)

        lines.append(
            f"Question : {example['question']}"
        )

        lines.append("")

        lines.append("SQL")

        lines.append(example["sql"])

        lines.append("=" * 60)

        lines.append("")

        return lines