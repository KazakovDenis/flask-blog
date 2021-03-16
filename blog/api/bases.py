from datetime import datetime

from flask_restful import Resource
from flask_restful.utils.cors import crossdomain
from flask_sqlalchemy import Model


class ModelView(Resource):
    model: Model
    template: str
    method_decorators = (
        crossdomain('*'),
    )

    @staticmethod
    def payload(**context):
        """Unify response body"""
        return {
            'errors': False,
            'datetime': str(datetime.utcnow()),
            'result': context,
        }

    def render(self, **context):
        """Implement for browsable view"""
        payload = self.payload(**context)
        return payload


class ListView(ModelView):
    """API endpoint for list of objects"""

    def get_objects(self):
        return self.model.query.all()

    def get(self):
        return self.render(
            objects=self.get_objects(),
        )


class DetailView(ModelView):
    """API endpoint for an object details"""

    def get_object(self, obj_id):
        selection = self.model.id == obj_id
        return self.model.query.filter(selection)

    def get(self, obj_id):
        return self.render(
            object=self.get_object(obj_id),
        )
