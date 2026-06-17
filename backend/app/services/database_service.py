from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.extractors.schema_extractor import SchemaExtractor
from app.services.schema_context import SchemaContext
from app.services.database_context import DatabaseContext


class DatabaseService:

    @staticmethod
    def _build_connection_url(config) -> str:
        """
        Build SQLAlchemy connection URL based on database type.
        """

        password = quote_plus(config.password)

        if config.db_type == "postgresql":
            return (
                f"postgresql+psycopg2://{config.username}:"
                f"{password}@{config.host}:"
                f"{config.port}/{config.database}"
            )

        elif config.db_type == "mysql":
            return (
                f"mysql+pymysql://{config.username}:"
                f"{password}@{config.host}:"
                f"{config.port}/{config.database}"
            )

        elif config.db_type == "sqlite":
            return f"sqlite:///{config.database}"

        raise ValueError("Unsupported database type")

    @classmethod
    def test_connection(cls, config):
        try:

            # Build connection URL
            connection_url = cls._build_connection_url(config)
            print("CONNECTION URL:", connection_url)
            # Create engine
            engine = create_engine(
                connection_url,
                pool_pre_ping=True
            )

            # Save engine globally
            DatabaseContext.set_engine(engine)

            print("ENGINE SAVED:", engine)

            # Test connection
            with engine.connect():
                pass

            # Extract schema
            schema = SchemaExtractor.extract(engine)

            # Save schema globally
            SchemaContext.save_schema(schema)

            print("SCHEMA SAVED:", schema)
            
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