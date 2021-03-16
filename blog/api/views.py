from datetime import datetime

from flask_restful import Resource, reqparse
from flask_sqlalchemy import Model

from .serializers import JSONModelSerializer


class BaseModelView(Resource):
    """API endpoint base class"""
    model: Model
    serializer = JSONModelSerializer
    template: str
    method_decorators = ()
    parser_cls = reqparse.RequestParser
    url_args = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = self._create_parser()
        if isinstance(self.serializer, type):
            self.serializer = self.serializer()

    def get_args(self):
        return self.parser.parse_args()

    @staticmethod
    def make_response(result, **context):
        """Implement for browsable view"""
        now = datetime.utcnow()
        payload = {
            'errors': False,
            'datetime': now.isoformat(),
            'result': result,
            **context
        }
        return payload

    def _create_parser(self):
        """Creates URL arguments parser"""
        parser = self.parser_cls()
        for arg in self.url_args:
            if isinstance(arg, str):
                self.parser.add_argument(arg)
            else:
                arg, kwargs = arg
                self.parser.add_argument(arg, **kwargs)
        return parser


class ListView(BaseModelView):
    """API endpoint for list of objects"""

    def get_objects(self):
        filters = self.get_args()
        objects = self.model.query.filter_by(**filters).all()
        return [self.serializer(obj) for obj in objects]

    def get(self):
        obj = self.get_objects()
        return self.make_response(obj)

    def post(self, *args, **kwargs):
        raise NotImplementedError


class DetailView(BaseModelView):
    """API endpoint for an object details"""

    def get_object(self, obj_id):
        obj = self.model.query.get(obj_id)
        return self.serializer(obj)

    def get(self, obj_id):
        obj = self.get_object(obj_id)
        return self.make_response(obj)

    def put(self, *args, **kwargs):
        raise NotImplementedError

    def patch(self, *args, **kwargs):
        return self.put(*args, **kwargs)
