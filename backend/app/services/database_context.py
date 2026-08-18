class DatabaseContext:
    
    engine = None
    connection_id = None

    @classmethod
    def set_engine(cls, engine):
        cls.engine = engine

    @classmethod
    def get_engine(cls):
        return cls.engine

    @classmethod
    def set_connection_id(cls, connection_id: int):
        cls.connection_id = connection_id

    @classmethod
    def get_connection_id(cls):
        return cls.connection_id

    @classmethod
    def clear_engine(cls):
        cls.engine = None
        cls.connection_id = None