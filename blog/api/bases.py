from datetime import datetime

from flask_restful import Resource, reqparse
from flask_sqlalchemy import Model

from .serializers import JSONModelSerializer


class BaseModelView(Resource):
    """API endpoint base class"""
    model: Model
    fields = ()
    serializer = JSONModelSerializer
    template: str
    method_decorators = ()
    parser_cls = reqparse.RequestParser
    url_args = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_parser()
        self.serializer = self.serializer(self.fields)

    def get_args(self):
        return self.parser.parse_args()

    @staticmethod
    def payload(**context):
        """Unify response body"""
        now = datetime.utcnow()
        return {
            'errors': False,
            'datetime': now.isoformat(),
            'result': context,
        }

    def render(self, **context):
        """Implement for browsable view"""
        payload = self.payload(**context)
        return payload

    def serialize(self, obj):
        return self.serializer(obj)

    def _create_parser(self):
        """Creates URL arguments parser"""
        self.parser = self.parser_cls()
        for arg in self.url_args:
            if isinstance(arg, str):
                self.parser.add_argument(arg)
            else:
                arg, kwargs = arg
                self.parser.add_argument(arg, **kwargs)


class ListView(BaseModelView):
    """API endpoint for list of objects"""

    def get_objects(self, **filters):
        objects = self.model.query.filter_by(**filters).all()
        return [self.serialize(obj) for obj in objects]

    def get(self):
        args = self.get_args()
        return self.render(
            objects=self.get_objects(**args),
        )

    def post(self, *args, **kwargs):
        raise NotImplementedError


class DetailView(BaseModelView):
    """API endpoint for an object details"""

    def get_object(self, obj_id):
        return self.model.query.get(obj_id)

    def get(self, obj_id):
        return self.render(
            object=self.get_object(obj_id),
        )

    def put(self, *args, **kwargs):
        raise NotImplementedError

    def patch(self, *args, **kwargs):
        return self.put(*args, **kwargs)
