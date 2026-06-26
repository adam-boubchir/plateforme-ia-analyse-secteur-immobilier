from app.database.session import SessionLocalMinistry
from app.audit.database_auditor import DatabaseAuditor
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def main():

    db = SessionLocalMinistry()

    try:

        auditor = DatabaseAuditor(db)

        report = auditor.build_report()

        print()

        print("=" * 80)
        print("DATABASE AUDIT REPORT")
        print("=" * 80)

        print()

        print("Metadata")
        print("--------------------------")
        print(report.metadata)

        print()

        print("Server")
        print("--------------------------")
        print(report.server)

        print()

        print("Statistics")
        print("--------------------------")
        print(report.statistics)
        print()
        print("Schemas")
        print("--------------------------")

        for schema in report.schemas:
            print(schema.name)

        print()
        print("Tables")
        print("--------------------------")

        for table in report.tables:
            print(f"{table.schema_name}.{table.name}")
        
        print()
        print("Columns")
        print("--------------------------")

        print(f"Total columns : {len(report.columns)}")

        print()
        print("Primary Keys")
        print("--------------------------")
        print(f"Total primary keys : {len(report.primary_keys)}")

        print()
        print("Foreign Keys")
        print("--------------------------")
        print(f"Total foreign keys : {len(report.foreign_keys)}")

        print()
        print("Views")
        print("--------------------------")
        print(f"Total views : {len(report.views)}")

        print()
        print("Indexes")
        print("--------------------------")
        print(f"Total indexes : {len(report.indexes)}")

        print()
        print("Table Statistics")
        print("--------------------------")

        for stat in report.table_statistics:
            print(
                f"{stat.schema_name}.{stat.table} : {stat.row_count} rows"
            )
        print()

        


    finally:

        db.close()


if __name__ == "__main__":

    main()