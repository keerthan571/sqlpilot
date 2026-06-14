from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.extractors.schema_extractor import SchemaExtractor


class DatabaseService:
    @staticmethod
    def _build_connection_url(config) -> str:
        """
        Build SQLAlchemy connection URL based on database type.
        """

        if config.db_type == "postgresql":
            return (
                f"postgresql+psycopg2://{config.username}:"
                f"{config.password}@{config.host}:"
                f"{config.port}/{config.database}"
            )

        elif config.db_type == "mysql":
            return (
                f"mysql+pymysql://{config.username}:"
                f"{config.password}@{config.host}:"
                f"{config.port}/{config.database}"
            )

        elif config.db_type == "sqlite":
            return f"sqlite:///{config.database}"

        raise ValueError("Unsupported database type")

    @classmethod
    def test_connection(cls, config):
        try:
            # Build URL
            connection_url = cls._build_connection_url(config)

            # Create engine
            engine = create_engine(
                connection_url,
                pool_pre_ping=True
            )

            # Verify connection
            with engine.connect() as connection:
             pass

            # Extract schema
            schema = SchemaExtractor.extract(engine)

            return {
                "success": True,
                "message": "Database connected successfully.",
                "database_type": config.db_type,
                "schema": schema
            }

        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "database_type": config.db_type,
                "schema": None
            }

        except SQLAlchemyError as e:
            return {
                "success": False,
                "message": str(e),
                "database_type": config.db_type,
                "schema": None
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}",
                "database_type": config.db_type,
                "schema": None
            }