from flask import request
from flask_restful import Resource, reqparse
from flask_sqlalchemy import Model

from .serializers import JSONModelSerializer
from ..factory import db


class BaseModelView(Resource):
    """API endpoint base class"""
    model: Model
    serializer = JSONModelSerializer
    template: str
    method_decorators = ()
    parser_cls = reqparse.RequestParser
    url_args = ()

    def __init__(self, *args, **kwargs):
        assert self.model, 'No model specified'
        super().__init__(*args, **kwargs)
        self.parser = self._create_parser()
        if isinstance(self.serializer, type):
            self.serializer = self.serializer()

    def get_args(self):
        return self.parser.parse_args()

    # todo: add status code
    @staticmethod
    def make_response(result, **context):
        """Implement for browsable view"""
        payload = {
            'errors': False,
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
        return self.model.query.filter_by(**filters).all()

    def get(self):
        payload = []
        objects = self.get_objects()
        if objects:
            # todo: 404 if no objects
            payload = [self.serializer(obj) for obj in objects]
        return self.make_response(payload)

    def post(self, *args, **kwargs):
        # noinspection PyCallingNonCallable
        obj = self.model(**request.json)
        db.session.add(obj)
        db.session.commit()
        payload = self.serializer(obj)
        return self.make_response(payload)


class DetailView(BaseModelView):
    """API endpoint for an object details"""

    def get_object(self, obj_id):
        return self.model.query.get(obj_id)

    def get(self, obj_id):
        payload = None
        obj = self.get_object(obj_id)
        if obj:
            # todo: 404 if no object
            payload = self.serializer(obj)
        return self.make_response(payload)

    def delete(self, obj_id):
        obj = self.get_object(obj_id)
        db.session.delete(obj)
        db.session.commit()
        return self.make_response('ok')

    def put(self, obj_id):
        obj = self.get_object(obj_id)
        for key, value in request.json.items():
            setattr(obj, key, value)
        db.session.commit()
        payload = self.serializer(obj)
        return self.make_response(payload)

    def patch(self, *args, **kwargs):
        return self.put(*args, **kwargs)
