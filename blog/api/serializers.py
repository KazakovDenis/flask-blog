from collections import abc
from datetime import date

from flask_sqlalchemy import Model


class BaseModelSerializer:
    """Model serializers base class"""
    fields = ()
    related = {}

    def __init__(self, *fields):
        if fields:
            self.fields = fields

    def __call__(self, obj):
        if isinstance(obj, abc.Iterable):
            return [self._convert(i) for i in obj]
        return self._convert(obj)

    def _convert(self, obj):
        """Serialize instance. The method to override."""
        raise NotImplementedError

    def _get_value(self, obj: Model, field: str):
        """Get converted value of a model field"""
        value = getattr(obj, field, None)
        if field in self.related:
            serializer = self.related[field]
            return serializer(value)

        if isinstance(value, date):
            value = value.isoformat()
        return value


class JSONModelSerializer(BaseModelSerializer):
    """Model to dict serializer"""

    def _convert(self, obj: Model):
        serialized = {}
        for field in self.fields:
            value = self._get_value(obj, field)
            serialized[field] = value
        return serialized


class PostSerializer(JSONModelSerializer):
    fields = ('id', 'title', 'body', 'created', 'slug', 'tags')
    related = {
        'tags': JSONModelSerializer('id', 'name', 'slug'),
    }


class TagSerializer(JSONModelSerializer):
    fields = ('id', 'name', 'slug', 'posts')
    related = {
        'posts': JSONModelSerializer('id', 'title', 'created', 'slug'),
    }
