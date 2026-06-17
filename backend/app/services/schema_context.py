class SchemaContext:
    
    schema = {}

    @classmethod
    def save_schema(cls, schema):
        cls.schema = schema

    @classmethod
    def get_schema(cls):
        return cls.schema