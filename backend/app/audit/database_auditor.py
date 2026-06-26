from datetime import datetime

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.audit.audit_models import (
    AuditMetadata,
    AuditReport,
    DatabaseServer,
    DatabaseStatistics,
    Schema,
    Table,
    Column,
    PrimaryKey,
    ForeignKey,
    View,
    Index,
    TableStatistics,
)

import logging

SYSTEM_SCHEMAS = {
    "sys",
    "guest",
    "INFORMATION_SCHEMA",
    "db_owner",
    "db_accessadmin",
    "db_backupoperator",
    "db_datareader",
    "db_datawriter",
    "db_ddladmin",
    "db_denydatareader",
    "db_denydatawriter",
    "db_securityadmin",
}

logger = logging.getLogger(__name__)


class DatabaseAuditor:
    """
    Analyze a SQL Server database and build an audit report.
    """

    def __init__(self, db: Session):

        self.db = db
        self.inspector = inspect(db.bind)

    def _safe_execute(
        self,
        loader,
        metadata: AuditMetadata,
        default
    ):
        """
        Execute a loader safely and record any error.
        """

        logger.info("Loading %s...", loader.__name__)

        try:
            return loader()

        except Exception as e:

            logger.exception("%s failed.", loader.__name__)

            metadata.success = False

            metadata.errors.append(
                f"{loader.__name__}: {e}"
            )

            return default

    def build_report(self) -> AuditReport:
        """
        Build the complete audit report.
        """

        logger.info("Starting database audit...")

        metadata = self._load_metadata()

        try:

            # Server information
            server = self._safe_execute(
                self._load_server,
                metadata,
                None
            )

            schemas = self._safe_execute(
                self._load_schemas,
                metadata,
                []
            )

            tables = self._safe_execute(
                self._load_tables,
                metadata,
                []
            )

            columns = self._safe_execute(
                self._load_columns,
                metadata,
                []
            )

            views = self._safe_execute(
                self._load_views,
                metadata,
                []
            )

            primary_keys = self._safe_execute(
                self._load_primary_keys,
                metadata,
                []
            )

            foreign_keys = self._safe_execute(
                self._load_foreign_keys,
                metadata,
                []
            )

            indexes = self._safe_execute(
                self._load_indexes,
                metadata,
                []
            )

            table_statistics = self._safe_execute(
                self._load_table_statistics,
                metadata,
                []
            )

            total_rows = sum(
                table.row_count
                for table in table_statistics
            ) if table_statistics else 0

            statistics = DatabaseStatistics(
                total_tables=len(tables),
                total_views=len(views),
                total_columns=len(columns),
                total_primary_keys=len(primary_keys),
                total_foreign_keys=len(foreign_keys),
                total_indexes=len(indexes),
                total_rows=total_rows,
            )

            if server is None:
                raise RuntimeError(
                    "Unable to load SQL Server information."
                )

            report = AuditReport(
                metadata=metadata,
                server=server,
                statistics=statistics,
                schemas=schemas,
                tables=tables,
                views=views,
                columns=columns,
                primary_keys=primary_keys,
                foreign_keys=foreign_keys,
                indexes=indexes,
                table_statistics=table_statistics,
            )

            logger.info("Database audit completed successfully.")

            return report

        except Exception as e:

            logger.exception("Database audit failed.")

            metadata.success = False
            metadata.errors.append(str(e))

            raise

    def _load_metadata(self) -> AuditMetadata:
        """
        Load audit metadata.
        """

        return AuditMetadata(
            generated_at=datetime.now()
        )

    def _load_server(self) -> DatabaseServer:
        """
        Load SQL Server information.
        """

        database_name = self.db.execute(
            text("SELECT DB_NAME()")
        ).scalar()

        server_name = self.db.execute(
            text("SELECT @@SERVERNAME")
        ).scalar()

        version = self.db.execute(
            text("SELECT @@VERSION")
        ).scalar()

        return DatabaseServer(
            server_name=str(server_name),
            database_name=str(database_name),
            sql_server_version=str(version),
        )

    def _load_schemas(self) -> list[Schema]:
        """
        Load all database schemas.
        """

        schemas = []

        for schema_name in self.inspector.get_schema_names():

            # Ignore SQL Server internal schemas if desired
            if schema_name in SYSTEM_SCHEMAS:
                continue

            schemas.append(
                Schema(
                    name=schema_name
                )
            )

        return sorted(schemas, key=lambda s: s.name)
    
    def _load_tables(self) -> list[Table]:
        """
        Load all user tables from every schema.
        """

        tables = []

        for schema in self.inspector.get_schema_names():

            if schema in SYSTEM_SCHEMAS:               
                continue

            for table_name in self.inspector.get_table_names(schema=schema):

                tables.append(
                    Table(
                        schema_name=schema,
                        name=table_name,
                        table_type="BASE TABLE"
                    )
                )

        return sorted(
            tables,
            key=lambda t: (t.schema_name, t.name)
        )
    
    def _load_columns(self) -> list[Column]:
        """
        Load all columns from all user tables.
        """

        columns = []

        for schema in self.inspector.get_schema_names():

            if schema in SYSTEM_SCHEMAS:               
                continue

            for table_name in self.inspector.get_table_names(schema=schema):

                table_columns = self.inspector.get_columns(
                    table_name,
                    schema=schema
                )

                for column in table_columns:

                    columns.append(
                        Column(
                            schema_name=schema,
                            table=table_name,
                            name=column["name"],
                            data_type=str(column["type"]),
                            nullable=column["nullable"],
                            max_length=None,
                            default_value=str(column.get("default"))
                            if column.get("default") is not None
                            else None,
                        )
                    )

        return sorted(
            columns,
            key=lambda c: (
                c.schema_name,
                c.table,
                c.name
            )
        )
    
    def _load_primary_keys(self) -> list[PrimaryKey]:
        """
        Load all primary keys from user tables.
        """

        primary_keys = []

        for schema in self.inspector.get_schema_names():

            if schema in SYSTEM_SCHEMAS:               
                continue

            for table_name in self.inspector.get_table_names(schema=schema):

                pk = self.inspector.get_pk_constraint(
                    table_name,
                    schema=schema
                )

                constrained_columns = pk.get("constrained_columns", [])

                for column in constrained_columns:

                    primary_keys.append(
                        PrimaryKey(
                            schema_name=schema,
                            table=table_name,
                            column=column
                        )
                    )

        return sorted(
            primary_keys,
            key=lambda pk: (
                pk.schema_name,
                pk.table,
                pk.column
            )
        )
    
    def _load_foreign_keys(self) -> list[ForeignKey]:
        """
        Load all foreign keys from user tables.
        """

        foreign_keys = []

        for schema in self.inspector.get_schema_names():

            if schema in SYSTEM_SCHEMAS:               
                continue

            for table_name in self.inspector.get_table_names(schema=schema):

                fks = self.inspector.get_foreign_keys(
                    table_name,
                    schema=schema
                )

                for fk in fks:

                    constrained_columns = fk.get("constrained_columns", [])
                    referred_columns = fk.get("referred_columns", [])

                    for source_column, target_column in zip(
                        constrained_columns,
                        referred_columns
                    ):

                        foreign_keys.append(
                            ForeignKey(
                                constraint_name=fk["name"],
                                source_schema=schema,
                                source_table=table_name,
                                source_column=source_column,
                                target_schema=fk["referred_schema"] or "dbo",
                                target_table=fk["referred_table"],
                                target_column=target_column,
                            )
                        )

        return sorted(
            foreign_keys,
            key=lambda fk: (
                fk.source_schema,
                fk.source_table,
                fk.constraint_name
            )
        )
    
    def _load_views(self) -> list[View]:
        """
        Load all database views.
        """

        views = []

        for schema in self.inspector.get_schema_names():

            if schema in SYSTEM_SCHEMAS:
                continue

            for view_name in self.inspector.get_view_names(schema=schema):

                views.append(
                    View(
                        schema_name=schema,
                        name=view_name
                    )
                )

        return sorted(
            views,
            key=lambda v: (
                v.schema_name,
                v.name
            )
        )
    
    def _load_indexes(self) -> list[Index]:
        """
        Load all indexes from user tables.
        """

        indexes = []

        for schema in self.inspector.get_schema_names():

            if schema in SYSTEM_SCHEMAS:               
                continue

            for table_name in self.inspector.get_table_names(schema=schema):

                table_indexes = self.inspector.get_indexes(
                    table_name,
                    schema=schema
                )

                for index in table_indexes:

                    indexes.append(
                        Index(
                            table=table_name,
                            name=index["name"],
                            index_type="NONCLUSTERED",
                            unique=index.get("unique", False),
                        )
                    )

        return sorted(
            indexes,
            key=lambda idx: (
                idx.table,
                idx.name
            )
        )
    
    def _load_table_statistics(self) -> list[TableStatistics]:
        """
        Load statistics for every user table.
        """

        statistics = []

        query = """
        SELECT
            s.name AS schema_name,
            t.name AS table_name,
            SUM(p.rows) AS row_count
        FROM sys.tables t
        JOIN sys.schemas s
            ON t.schema_id = s.schema_id
        JOIN sys.partitions p
            ON t.object_id = p.object_id
        WHERE p.index_id IN (0,1)
        GROUP BY s.name, t.name
        ORDER BY s.name, t.name
        """

        result = self.db.execute(text(query))

        for row in result:

            statistics.append(
                TableStatistics(
                    schema_name=row.schema_name,
                    table=row.table_name,
                    row_count=int(row.row_count),
                    size_mb=0.0
                )
            )

        return statistics