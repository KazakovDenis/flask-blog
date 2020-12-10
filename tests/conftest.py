import pytest

from blog.config import Configuration
from blog.factory import create_app
from blog.init import register_blueprints
from blog.models import Tag, db, user_datastore as datastore


@pytest.fixture(scope='session')
def app(request):
    """Create and configure an app instance for tests"""
    Configuration.TESTING = True
    Configuration.SECRET_KEY = 'secret'
    Configuration.WTF_CSRF_ENABLED = False
    Configuration.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    migrations_dir = 'test_migrations'
    test_app = create_app(Configuration, migrations_dir=migrations_dir)

    ctx = test_app.app_context()
    ctx.push()
    db.create_all()
    register_blueprints(test_app)

    tag = Tag(name='projects')
    db.session.add(tag)
    db.session.commit()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return test_app


@pytest.fixture
def client(app):
    """A test client for the app"""
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope='session')
def credentials():
    """Credentials for the test user"""
    return {'email': 'user@test.com', 'password': 'p@$$w0rd'}


@pytest.fixture(scope='session')
def admin(credentials):
    """Test user"""
    test_user = datastore.create_user(active=True, **credentials)
    test_role = datastore.create_role(name='admin')
    datastore.add_role_to_user(test_user, test_role)
    db.session.commit()
    return test_user
