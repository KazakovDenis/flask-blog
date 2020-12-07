from dynamic_sitemap import FlaskSitemap

from app.blog import app
from app.models import Post, Tag
from app.services import sm_log


class SMConfig:
    DEBUG = False
    FOLDER = ('static',)
    TEMPLATE_FOLDER = ('app', 'templates',)
    # todo: что за '/blog/./' ???
    IGNORED = ['/admin', '/edit', '/static', '/upload', '/blog/./']
    INDEX_PRIORITY = 1.0
    LOGGER = sm_log


sitemap = FlaskSitemap(app, 'https://kazakov.ru.net', orm='sqlalchemy', config_obj=SMConfig)
sitemap.add_rule('/blog', Post, loc_attr='slug', lastmod_attr='created')
sitemap.add_rule('/blog/tag', Tag, loc_attr='slug', priority=0.8)
sm_view = sitemap.view


if __name__ == '__main__':
    sitemap.build_static()
