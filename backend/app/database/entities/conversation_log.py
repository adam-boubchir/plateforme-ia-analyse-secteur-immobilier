from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

from app.database.entities.base import Base


class ConversationLog(Base):
    """
    Stores the complete execution trace of one SQL Agent request.

    One log corresponds to one user question.
    """

    __tablename__ = "conversation_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )

    message_id = Column(
        Integer,
        ForeignKey("conversation_messages.id"),
        nullable=True,
        index=True,
    )

    # -------------------------------
    # User Question
    # -------------------------------

    question = Column(
        Text,
        nullable=False,
    )

    # -------------------------------
    # Context Generation
    # -------------------------------

    selected_tables = Column(
        Text,
        nullable=True,
    )

    business_knowledge = Column(
        Text,
        nullable=True,
    )

    join_knowledge = Column(
        Text,
        nullable=True,
    )

    forbidden_joins = Column(
        Text,
        nullable=True,
    )

    semantic_context = Column(
        Text,
        nullable=True,
    )

    sql_patterns = Column(
        Text,
        nullable=True,
    )

    full_context = Column(
        Text,
        nullable=True,
    )

    # -------------------------------
    # Prompt
    # -------------------------------

    prompt = Column(
        Text,
        nullable=True,
    )

    # -------------------------------
    # SQL Generation
    # -------------------------------

    generated_sql = Column(
        Text,
        nullable=True,
    )

    validated_sql = Column(
        Text,
        nullable=True,
    )

    # -------------------------------
    # SQL Result
    # -------------------------------

    sql_result = Column(
        Text,
        nullable=True,
    )

    formatted_answer = Column(
        Text,
        nullable=True,
    )

    # -------------------------------
    # Execution Information
    # -------------------------------

    execution_time_ms = Column(
        Integer,
        nullable=True,
    )

    status = Column(
        Text,
        nullable=False,
        default="SUCCESS",
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    # -------------------------------
    # Audit
    # -------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )