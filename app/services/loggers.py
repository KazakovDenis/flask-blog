import logging
from os.path import join

from app.blog import app
from app.config import *

# app
log = app.logger
log.setLevel(LOG_LEVEL)
fh = logging.FileHandler(join(PATH, 'log', 'flask', 'app.log'), encoding='utf-8')
fh.setLevel(LOG_LEVEL)
fh.setFormatter(logging.Formatter(LOG_FORMAT))
log.addHandler(fh)

# sitemap
sm_log = logging.getLogger('sitemap')
sm_log.setLevel(LOG_LEVEL)
smh = logging.FileHandler(join(PATH, 'log', 'flask', 'sitemap.log'), encoding='utf-8')
smh.setLevel(LOG_LEVEL)
smh.setFormatter(logging.Formatter(LOG_FORMAT))
sm_log.addHandler(fh)
