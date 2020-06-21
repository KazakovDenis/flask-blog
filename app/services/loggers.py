import logging

from app.blog import app
from app.config import *


LOG_DIR = os.path.join(PATH, 'log')
for name in ('flask', 'gunicorn'):
    folder = os.path.join(LOG_DIR, name)
    os.makedirs(folder, exist_ok=True)


# app
log = app.logger
log.setLevel(LOG_LEVEL)
fh = logging.FileHandler(os.path.join(LOG_DIR, 'flask', 'app.log'), encoding='utf-8')
fh.setLevel(LOG_LEVEL)
fh.setFormatter(logging.Formatter(LOG_FORMAT))
log.addHandler(fh)

# sitemap
sm_log = logging.getLogger('sitemap')
sm_log.setLevel(LOG_LEVEL)
smh = logging.FileHandler(os.path.join(LOG_DIR, 'flask', 'sitemap.log'), encoding='utf-8')
smh.setLevel(LOG_LEVEL)
smh.setFormatter(logging.Formatter(LOG_FORMAT))
sm_log.addHandler(fh)
