from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.extractors.schema_extractor import SchemaExtractor
from app.services.schema_context import SchemaContext
from app.services.database_context import DatabaseContext
from app.services.saved_connection_service import SavedConnectionService

class DatabaseService:

    @staticmethod
    def _build_connection_url(config) -> str:

        if isinstance(config, dict):
            db_type = config["db_type"]
            username = config["username"]
            password = config["password"]
            host = config["host"]
            port = config["port"]
            database = config["database_name"]

        else:
            db_type = config.db_type
            username = config.username
            password = config.password
            host = config.host
            port = config.port
            database = config.database

        password = quote_plus(password)

        if db_type == "postgresql":
            return (
                f"postgresql+psycopg2://{username}:"
                f"{password}@{host}:{port}/{database}"
            )

        elif db_type == "mysql":
            return (
                f"mysql+pymysql://{username}:"
                f"{password}@{host}:{port}/{database}"
            )

        elif db_type == "sqlite":
            return f"sqlite:///{database}"

        raise ValueError("Unsupported database type")

    @classmethod
    def test_connection(cls, config):
        try:

            # Build connection URL
            connection_url = cls._build_connection_url(config)
            print(
                "CONNECTING TO DATABASE:",
                config.db_type,
                config.host,
                config.port,
                config.database
            )
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

            # Save connection securely
            saved_connection_id = SavedConnectionService.save(config)

            print(
                "SAVED CONNECTION ID:",
                saved_connection_id
            )

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

    @classmethod
    def reconnect(cls, connection_id: int):

        try:
            # Retrieve saved credentials internally
            saved = SavedConnectionService.get_connection(
                connection_id
            )

            if not saved:
                return {
                    "success": False,
                    "message": "Saved connection not found.",
                    "database_type": "",
                    "schema": None
                }

            # Build connection URL
            connection_url = cls._build_connection_url(saved)

            print(
                "RECONNECTING TO SAVED DATABASE:",
                saved["db_type"],
                saved["host"],
                saved["port"],
                saved["database_name"]
            )

            # Create engine
            engine = create_engine(
                connection_url,
                pool_pre_ping=True
            )

            # Test connection
            with engine.connect():
                pass

            # Save engine globally
            DatabaseContext.set_engine(engine)

            print(
                "RECONNECTED ENGINE SAVED:",
                engine
            )

            # Extract schema
            schema = SchemaExtractor.extract(engine)

            # Save schema globally
            SchemaContext.save_schema(schema)

            print(
                "RECONNECTED SCHEMA SAVED:",
                schema
            )

            return {
                "success": True,
                "message": "Database reconnected successfully.",
                "database_type": saved["db_type"],
                "schema": schema
            }

        except ValueError as e:

            return {
                "success": False,
                "message": str(e),
                "database_type": "",
                "schema": None
            }

        except SQLAlchemyError as e:

            return {
                "success": False,
                "message": str(e),
                "database_type": "",
                "schema": None
            }

        except Exception as e:

            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}",
                "database_type": "",
                "schema": None
            }
