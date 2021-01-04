from configparser import ConfigParser
from pathlib import Path


ROOT = Path(__file__).parent.absolute()
cp = ConfigParser()
cp.read(ROOT / '.env')


def get_env(name):
    return cp.get('env', name)


# common
DOMAIN = get_env('DOMAIN')

# database
DB_USER = get_env('DB_USER')
DB_PASS = get_env('DB_PASS')
DB_ADDRESS = get_env('DB_ADDRESS')
DATABASE_URI = None
if DB_USER and DB_PASS and DB_ADDRESS:
    DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_ADDRESS}/blog'

# Github webhooks
GH_SECRET = get_env('GH_SECRET')
GH_SENDER_ID = get_env('GH_SENDER_ID')
GH_REPO_ID = get_env('GH_REPO_ID')

# logging
LOG_LEVEL = 30
LOG_FORMAT = "[%(asctime)s] @%(name)s  %(levelname)s in %(module)s: %(message)s"
LOG_DIR = ROOT.parent / 'log'


# Flask app
class Configuration:
    DEBUG = False
    SQLALCHEMY_ECHO = DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SECRET_KEY = get_env('FLASK_SECRET')
    UPLOAD_FOLDER = Path(ROOT, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # flask security
    SECURITY_PASSWORD_SALT = get_env('FLASK_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
