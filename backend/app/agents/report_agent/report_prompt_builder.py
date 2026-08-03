from __future__ import annotations

import json

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

Your mission is to transform structured analytical data into a clear,
professional and objective business report.

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
- Base every statement on the supplied dataset.

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

Provide a short overview.

# Objective

Explain the purpose of the analysis.

# Dataset Overview

Describe the dataset.

# Methodology

Explain that the report is generated from SQL query results and statistical analysis.

# Statistical Analysis

Interpret the computed statistics.

# Key Findings

Highlight the most important findings.

# Recommended Visualizations

Explain which charts should be displayed and why.

# Business Recommendations

Provide practical recommendations supported by the data.

# Conclusion

Summarize the report.
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

    def build(
        self,
        *,
        question: str,
        analysis: ReportAnalysis,
        charts: list[ChartRecommendation],
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
- never invent numerical values;
- never infer unsupported conclusions;
- explain the statistical results;
- reference important indicators;
- describe trends only if they are present;
- explain anomalies only if supported by statistics;
- provide practical recommendations based on the analysis;
- use Markdown formatting;
- remain objective and concise.

==================================================
OUTPUT FORMAT
==================================================

Generate the report using exactly this structure:

# Executive Summary

...

# Objective

...

# Dataset Overview

...

# Methodology

...

# Statistical Analysis

...

# Key Findings

...

# Recommended Visualizations

...

# Business Recommendations

...

# Conclusion
"""

        return prompt.strip()


__all__ = (
    "ReportPromptBuilder",
)