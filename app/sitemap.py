import logging
from os.path import join

from blog import app
from models import Post, Tag
from sitemap_ext import FlaskSitemap


log = logging.getLogger('sitemap')
log.setLevel(30)

fh = logging.FileHandler(join('..', 'log', 'flask', 'sitemap.log'), encoding='utf-8')
fh.setLevel(30)
fh.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
log.addHandler(fh)


class SMConfig:
    DEBUG = False
    FOLDER = ('static',)
    IGNORED = ['/admin', '/edit', '/static', '/upload']
    INDEX_PRIORITY = 1.0
    LOGGER = log


sitemap = FlaskSitemap(app, 'https://kazakov.ru.net', config_obj=SMConfig)
sitemap.add_rule('/blog', Post, lastmod='created')
sitemap.add_rule('/blog/tag', Tag, priority=0.8)
sm_view = sitemap.view


if __name__ == '__main__':
    sitemap.build_static()
