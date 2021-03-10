from flask import render_template, Flask
from flask_security import SQLAlchemyUserDatastore
from sqlalchemy.exc import IntegrityError

from .admin import create_admin
from .config import Configuration, DOMAIN, INITIAL_FIXTURES
from .factory import db, create_app
from .models import user_datastore
from .services.fixture import load_fixtures
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


def load_initial_data():
    """Load instances necessary to start the app"""
    for obj in load_fixtures(INITIAL_FIXTURES):
        try:
            db.session.add(obj)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def init_app(config: type = Configuration,
             datastore: SQLAlchemyUserDatastore = user_datastore,
             domain: str = DOMAIN) -> Flask:
    """Initialize the app"""
    application = create_app(config, datastore)
    register_blueprints(application)
    create_sitemap(application, domain=domain)
    return application
