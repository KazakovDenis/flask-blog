from flask import render_template, Flask
from flask_security import SQLAlchemyUserDatastore

from .admin import create_admin
from .config import Configuration, DOMAIN
from .factory import db, create_app
from .models import user_datastore
from .services.sitemap import create_sitemap

from .api.blueprint import api
from .main.blueprint import main
from .posts.blueprint import posts


def register_blueprints(app: Flask):
    """Connect blueprint and views to the app"""
    @app.errorhandler(404)
    def page_not_found(event):
        return render_template('404.html'), 404

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(posts, url_prefix='/blog/')
    app.register_blueprint(api, url_prefix='/api/')
    create_admin(app, db)


def init_app(config: type = Configuration,
             datastore: SQLAlchemyUserDatastore = user_datastore,
             domain: str = DOMAIN) -> Flask:
    """Initialize the app"""
    application = create_app(config, datastore)
    register_blueprints(application)
    create_sitemap(application, domain=domain)
    return application
