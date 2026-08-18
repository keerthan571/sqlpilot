from sqlalchemy import create_engine, text


class QueryHistoryService:

    DB_PATH = "sqlite:///sqlpilot_history.db"

    @classmethod
    def _get_engine(cls):

        return create_engine(
            cls.DB_PATH,
            pool_pre_ping=True
        )

    @classmethod
    def initialize(cls):

        engine = cls._get_engine()

        with engine.begin() as conn:

            # Create table for fresh installations
            conn.execute(
                text("""
                    CREATE TABLE IF NOT EXISTS queries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        connection_id INTEGER NOT NULL,
                        question TEXT NOT NULL,
                        generated_sql TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            )

            # Check existing table columns
            columns = conn.execute(
                text("PRAGMA table_info(queries)")
            ).fetchall()

            column_names = {
                row._mapping["name"]
                for row in columns
            }

            # Upgrade existing history database
            if "connection_id" not in column_names:

                conn.execute(
                    text("""
                        ALTER TABLE queries
                        ADD COLUMN connection_id INTEGER
                    """)
                )

    @classmethod
    def save_query(
        cls,
        connection_id: int,
        question: str,
        generated_sql: str
    ):

        cls.initialize()

        if connection_id is None:
            raise ValueError(
                "No active database connection."
            )

        engine = cls._get_engine()

        insert_sql = text("""
            INSERT INTO queries (
                connection_id,
                question,
                generated_sql
            )
            VALUES (
                :connection_id,
                :question,
                :generated_sql
            )
        """)

        with engine.begin() as conn:

            conn.execute(
                insert_sql,
                {
                    "connection_id": connection_id,
                    "question": question,
                    "generated_sql": generated_sql
                }
            )