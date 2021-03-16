from datetime import date

from flask_sqlalchemy import Model


def prepare(value):
    """Serialize model fields values"""
    if isinstance(value, date):
        value = value.isoformat()
    return value


class BaseModelSerializer:
    """Model serializers base class"""

    def __init__(self, fields: tuple):
        self.fields = fields

    def __call__(self, obj: Model):
        raise NotImplementedError


class JSONModelSerializer(BaseModelSerializer):
    """Model to dict serializer"""

    def __call__(self, obj: Model):
        serialized = {}
        for field in self.fields:
            value = getattr(obj, field, None)
            serialized[field] = prepare(value)
        return serialized
