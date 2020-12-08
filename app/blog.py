from .admin import create_admin
from .factory import create_app, db
from .models import user_datastore
from .services.sitemap import create_sitemap

from .posts.blueprint import posts
from .api.blueprint import api


app = create_app(datastore=user_datastore)
create_admin(app, db)
app.register_blueprint(posts, url_prefix='/blog/')
app.register_blueprint(api, url_prefix='/api/')
sitemap = create_sitemap(app)
