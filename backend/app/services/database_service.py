from sqlalchemy import create_engine


class DatabaseService:

    @staticmethod
    def test_connection(config):
        try:
            if config.db_type == "postgresql":
                url = (
                    f"postgresql+psycopg2://{config.username}:"
                    f"{config.password}@{config.host}:"
                    f"{config.port}/{config.database}"
                )

            elif config.db_type == "mysql":
                url = (
                    f"mysql+pymysql://{config.username}:"
                    f"{config.password}@{config.host}:"
                    f"{config.port}/{config.database}"
                )

            else:
                return False, "Unsupported database"

            engine = create_engine(url)

            with engine.connect():
                pass

            return True, "Connection Successful"

        except Exception as e:
            return False, str(e)