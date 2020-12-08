from flask_security import SQLAlchemyUserDatastore, Security

from.factory import create_app, db


app = create_app()

from app.services import log
from app.posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/blog/')

from app.api.blueprint import api
app.register_blueprint(api, url_prefix='/api/')

from app.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from app.admin import admin
from app.sitemap import sm_view
app.add_url_rule('/sitemap.xml', endpoint='sitemap', view_func=sm_view)
