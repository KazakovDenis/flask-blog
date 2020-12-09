import os
from pathlib import Path


# common
DOMAIN = 'https://kazakov.ru.net'
PATH = Path(__file__).parent.absolute()

# database
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_ADDRESS = os.environ.get('DB_ADDRESS', '')

# Github webhooks
GH_SECRET = os.environ.get('GH_SECRET')
GH_SENDER_ID = os.environ.get('GH_SENDER_ID')
GH_REPO_ID = os.environ.get('GH_REPO_ID')

# logging
LOG_LEVEL = 30
LOG_FORMAT = "[%(asctime)s] @%(name)s  %(levelname)s in %(module)s: %(message)s"
LOG_DIR = PATH.parent / 'log'


# Flask app
class Configuration:
    DEBUG = False
    SQLALCHEMY_ECHO = DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_ADDRESS}/blog'
    SECRET_KEY = os.environ.get('FLASK_SECRET')
    UPLOAD_FOLDER = os.path.join(PATH, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # flask security
    SECURITY_PASSWORD_SALT = os.environ.get('FLASK_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
