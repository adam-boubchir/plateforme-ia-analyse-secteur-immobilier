from __future__ import annotations

__all__ = [
    "SQLAgentError",
    "EmptySQLException",
    "CannotGenerateSQLException",
]


class SQLAgentError(Exception):
    """
    Base exception for all SQL Agent errors.
    """


class EmptySQLQueryException(SQLAgentError):
    """
    Raised when the generated SQL query is empty.
    """


class CannotGenerateSQLException(SQLAgentError):
    """
    Raised when the LLM cannot generate a valid SQL query.
    """