from flask_security import SQLAlchemyUserDatastore, Security

from .admin import create_admin
from .factory import create_app, db
from .sitemap import create_sitemap


app = create_app()
create_admin(app, db)

from app.posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/blog/')

from app.api.blueprint import api
app.register_blueprint(api, url_prefix='/api/')

from app.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

sitemap = create_sitemap(app)
app.add_url_rule('/sitemap.xml', endpoint='sitemap', view_func=sitemap.view)
