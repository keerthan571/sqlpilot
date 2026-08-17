class DatabaseContext:
    
    engine = None

    @classmethod
    def set_engine(cls, engine):
        cls.engine = engine

    @classmethod
    def get_engine(cls):
        return cls.engine

    @classmethod
    def clear_engine(cls):
        cls.engine = None