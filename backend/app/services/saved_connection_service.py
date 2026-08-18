import os

from cryptography.fernet import Fernet
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()


class SavedConnectionService:

    DB_PATH = "sqlite:///sqlpilot_connections.db"

    @classmethod
    def _get_cipher(cls):
        key = os.getenv("SQLPILOT_ENCRYPTION_KEY")

        if not key:
            raise ValueError(
                "SQLPILOT_ENCRYPTION_KEY is not configured."
            )

        return Fernet(key.encode())

    @classmethod
    def _get_engine(cls):
        return create_engine(
            cls.DB_PATH,
            pool_pre_ping=True
        )

    @classmethod
    def initialize(cls):

        engine = cls._get_engine()

        with engine.begin() as connection:

            connection.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS saved_connections (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        db_type TEXT NOT NULL,
                        host TEXT NOT NULL,
                        port INTEGER NOT NULL,
                        username TEXT NOT NULL,
                        encrypted_password TEXT NOT NULL,
                        database_name TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                        UNIQUE (
                            db_type,
                            host,
                            port,
                            username,
                            database_name
                        )
                    )
                    """
                )
            )

    @classmethod
    def save(cls, config):

        cls.initialize()

        if config.db_type == "sqlite":
            name = config.database
            host = "local"
            port = 0
            username = "local"
        else:
            name = f"{config.db_type}_{config.database}"
            host = config.host
            port = config.port
            username = config.username

        cipher = cls._get_cipher()

        encrypted_password = cipher.encrypt(
            config.password.encode()
        ).decode()

        engine = cls._get_engine()

        with engine.begin() as connection:

            existing = connection.execute(
                text(
                    """
                    SELECT id
                    FROM saved_connections
                    WHERE
                        db_type = :db_type
                        AND host = :host
                        AND port = :port
                        AND username = :username
                        AND database_name = :database_name
                    """
                ),
                {
                    "db_type": config.db_type,
                    "host": host,
                    "port": port,
                    "username": username,
                    "database_name": config.database
                }
            ).fetchone()

            if existing:
                return existing.id

            result = connection.execute(
                text(
                    """
                    INSERT INTO saved_connections (
                        name,
                        db_type,
                        host,
                        port,
                        username,
                        encrypted_password,
                        database_name
                    )
                    VALUES (
                        :name,
                        :db_type,
                        :host,
                        :port,
                        :username,
                        :encrypted_password,
                        :database_name
                    )
                    """
                ),
                {
                    "name": name,
                    "db_type": config.db_type,
                    "host": host,
                    "port": port,
                    "username": username,
                    "encrypted_password": encrypted_password,
                    "database_name": config.database
                }
            )

            return result.lastrowid

    @classmethod
    def list_connections(cls):

        cls.initialize()

        engine = cls._get_engine()

        with engine.connect() as connection:

            result = connection.execute(
                text(
                    """
                    SELECT
                        id,
                        name,
                        db_type,
                        host,
                        port,
                        username,
                        database_name,
                        created_at
                    FROM saved_connections
                    ORDER BY created_at DESC
                    """
                )
            )

            return [
                dict(row._mapping)
                for row in result
            ]

    @classmethod
    def get_connection(cls, connection_id: int):

        cls.initialize()

        engine = cls._get_engine()

        with engine.connect() as connection:

            result = connection.execute(
                text(
                    """
                    SELECT
                        id,
                        name,
                        db_type,
                        host,
                        port,
                        username,
                        encrypted_password,
                        database_name
                    FROM saved_connections
                    WHERE id = :id
                    """
                ),
                {
                    "id": connection_id
                }
            )

            row = result.fetchone()

            if not row:
                return None

            data = dict(row._mapping)

        cipher = cls._get_cipher()

        data["password"] = cipher.decrypt(
            data.pop("encrypted_password").encode()
        ).decode()

        return data

    @classmethod
    def delete(cls, connection_id: int):

        cls.initialize()

        engine = cls._get_engine()

        with engine.begin() as connection:

            result = connection.execute(
                text(
                    """
                    DELETE FROM saved_connections
                    WHERE id = :id
                    """
                ),
                {
                    "id": connection_id
                }
            )

            return result.rowcount > 0