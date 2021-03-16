from flask import Blueprint
from flask_restful import Api

from .resources import PostApi, PostListApi, TagApi, TagListApi


api_bp = Blueprint('api', __name__, template_folder='templates')
api = Api(api_bp)
api.add_resource(PostListApi, 'posts/')
api.add_resource(PostApi, 'posts/<int:obj_id>/')
api.add_resource(TagListApi, 'tags/')
api.add_resource(TagApi, 'tags/<int:obj_id>/')
