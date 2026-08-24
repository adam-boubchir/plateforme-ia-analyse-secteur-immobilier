from __future__ import annotations

import json
from typing import Any

from app.agents.report_agent.report_models import (
    ReportAnalysis,
)
from app.visualization.models import (
    ChartRecommendation,
)


class ReportPromptBuilder:
    """
    Build the prompt sent to the language model.

    This component is responsible only for prompt construction.
    It does not perform any LLM inference.
    """

    _SYSTEM_PROMPT = """
You are a Senior Business Intelligence Analyst specialized in real estate,
urban planning, market intelligence and statistical reporting.

Your mission is to transform structured analytical data and SQL query
results into a clear, professional and objective business report.

========================
GENERAL RULES
========================

- Use ONLY the supplied information.
- Never invent values.
- Never estimate missing information.
- Never fabricate trends.
- Never assume causes that are not supported by the data.
- If some information is unavailable simply ignore it.
- Use professional business language.
- Write concise but informative paragraphs.
- Highlight important trends.
- Explain anomalies only if supported by statistics.
- Base every statement on the supplied dataset and query results.

========================
QUESTION-FIRST RULES
========================

The user's exact question has priority over general statistical analysis.

- Always answer the user's exact question first.
- The report must directly address what the user asked.
- If the user asks "Quels sont", "Quels", "Lesquels", "Which",
  "What are", "List", or asks for entities satisfying a condition,
  explicitly identify the entities that satisfy the condition.
- Do NOT replace a requested list of entities with aggregate statistics.
- Use the supplied QUERY RESULTS to identify the requested entities.
- Statistical summaries are complementary and must not replace the
  requested results.
- If the query results contain the requested entities, present them
  clearly in the report.
- When appropriate, use a Markdown table to present the requested
  entities and their relevant values.
- Do not omit the requested entities merely because the dataset contains
  many rows.
- If there are many matching entities, clearly state the total number
  and provide the complete list when practical using the supplied data.
- Never invent or reconstruct missing rows.
- Do not change the meaning of the user's question.
- Do not introduce MAX, MIN, AVG, SUM, COUNT or another aggregation
  as a substitute for the user's requested result unless that
  aggregation is explicitly present in the supplied query results or
  is required to describe the returned data.

========================
WRITING STYLE
========================

The report must be written as a professional analytical report.

Use Markdown.

Use:

# Titles

## Sections

### Subsections

Use bullet lists whenever appropriate.

Use Markdown tables if useful.

Avoid unnecessary repetition.

========================
EXPECTED REPORT STRUCTURE
========================

# Executive Summary

Provide a short overview that directly answers the user's question.

# Objective

Explain the purpose of the analysis and restate the analytical objective
without changing its meaning.

# Dataset Overview

Describe the dataset.

# Methodology

Explain that the report is generated from SQL query results and
statistical analysis.

# Statistical Analysis

Interpret the computed statistics.

# Key Findings

Highlight the most important findings and explicitly present the
entities requested by the user when applicable.

# Recommended Visualizations

Explain which charts should be displayed and why.

# Business Recommendations

Provide practical recommendations supported by the data.

# Conclusion

Summarize the report and directly answer the original question.
""".strip()

    @staticmethod
    def _serialize_statistics(
        analysis: ReportAnalysis,
    ) -> list[dict]:
        """
        Convert statistics into JSON-serializable dictionaries.
        """

        return [
            {
                "column": stat.column,
                "minimum": stat.minimum,
                "maximum": stat.maximum,
                "average": stat.average,
                "median": stat.median,
                "std": stat.std,
                "total": stat.total,
            }
            for stat in analysis.statistics.statistics
        ]

    @staticmethod
    def _serialize_charts(
        charts: list[ChartRecommendation],
    ) -> list[dict]:
        """
        Convert chart recommendations into dictionaries.
        """

        return [
            {
                "type": chart.chart_type.value,
                "title": chart.title,
                "x_axis": chart.x_axis,
                "y_axis": chart.y_axis,
                "reasons": list(chart.reasons),
            }
            for chart in charts
        ]

    @staticmethod
    def _serialize_insights(
        analysis: ReportAnalysis,
    ) -> list[dict]:
        """
        Convert business insights into dictionaries.
        """

        return [
            {
                "title": insight.title,
                "description": insight.description,
            }
            for insight in analysis.insights
        ]

    @staticmethod
    def _serialize_rows(
        rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Convert SQL query results into JSON-serializable dictionaries.

        The rows are the actual results returned by the SQL query and are
        provided to the LLM so that it can answer entity-level questions
        precisely instead of relying only on aggregate statistics.
        """

        serialized_rows: list[dict[str, Any]] = []

        for row in rows:
            serialized_row: dict[str, Any] = {}

            for key, value in row.items():

                # Handle common non-JSON-serializable values safely.
                if hasattr(value, "isoformat"):
                    serialized_row[key] = value.isoformat()
                else:
                    serialized_row[key] = value

            serialized_rows.append(serialized_row)

        return serialized_rows

    def build(
        self,
        *,
        question: str,
        analysis: ReportAnalysis,
        charts: list[ChartRecommendation],
        rows: list[dict[str, Any]],
    ) -> str:
        """
        Build the complete prompt sent to the LLM.
        """

        dataset = analysis.dataset

        statistics = self._serialize_statistics(
            analysis,
        )

        insights = self._serialize_insights(
            analysis,
        )

        chart_data = self._serialize_charts(
            charts,
        )

        query_results = self._serialize_rows(
            rows,
        )

        prompt = f"""
{self._SYSTEM_PROMPT}

==================================================
REPORT TYPE
==================================================

{analysis.report_type.value}

==================================================
USER QUESTION
==================================================

{question}

==================================================
QUERY RESULTS
==================================================

IMPORTANT:
The following rows are the actual results returned by the SQL query
executed for the user's question.

Use these rows as the primary source for answering the user's exact
question.

Do not replace these results with generalizations based only on
statistical summaries.

{json.dumps(
    query_results,
    indent=2,
    ensure_ascii=False,
    default=str,
)}

==================================================
DATASET OVERVIEW
==================================================

Rows:
{dataset.row_count}

Columns:
{dataset.column_count}

Column Names:

{json.dumps(
    dataset.columns,
    indent=2,
    ensure_ascii=False,
)}

Numeric Columns:

{json.dumps(
    dataset.numeric_columns,
    indent=2,
    ensure_ascii=False,
)}

Categorical Columns:

{json.dumps(
    dataset.categorical_columns,
    indent=2,
    ensure_ascii=False,
)}

Datetime Columns:

{json.dumps(
    dataset.datetime_columns,
    indent=2,
    ensure_ascii=False,
)}

Geographic Columns:

{json.dumps(
    dataset.geographic_columns,
    indent=2,
    ensure_ascii=False,
)}

==================================================
STATISTICAL SUMMARY
==================================================

{json.dumps(
    statistics,
    indent=2,
    ensure_ascii=False,
)}

==================================================
BUSINESS INSIGHTS
==================================================

{json.dumps(
    insights,
    indent=2,
    ensure_ascii=False,
)}

==================================================
RECOMMENDED VISUALIZATIONS
==================================================

{json.dumps(
    chart_data,
    indent=2,
    ensure_ascii=False,
)}

==================================================
REPORT WRITING INSTRUCTIONS
==================================================

Write a professional business report.

The report MUST:

- strictly use the supplied information;
- answer the user's exact question;
- use the QUERY RESULTS as the primary source for the requested result;
- never invent numerical values;
- never invent entities or rows;
- never infer unsupported conclusions;
- explain the statistical results;
- reference important indicators;
- describe trends only if they are present;
- explain anomalies only if supported by statistics;
- provide practical recommendations based on the analysis;
- use Markdown formatting;
- remain objective and concise.

If the user's question asks for a list of entities satisfying a condition,
the report MUST explicitly identify those entities from QUERY RESULTS.

Do not provide only minimum, maximum, average, median or other aggregate
statistics when the user explicitly asks which entities satisfy a condition.

The requested result must appear clearly in either the Executive Summary
or Key Findings section, preferably both when appropriate.

==================================================
OUTPUT FORMAT
==================================================

Generate the report using exactly this structure:

# Executive Summary

... direct answer to the user's question ...

# Objective

...

# Dataset Overview

...

# Methodology

...

# Statistical Analysis

...

# Key Findings

... requested entities and important findings ...

# Recommended Visualizations

...

# Business Recommendations

...

# Conclusion

... direct conclusion answering the user's question ...
"""

        return prompt.strip()


__all__ = (
    "ReportPromptBuilder",
)