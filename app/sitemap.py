from dynamic_sitemap import FlaskSitemap

from app.models import Post, Tag


class SMConfig:
    DEBUG = False
    FOLDER = ('static',)
    TEMPLATE_FOLDER = ('app', 'templates',)
    # todo: что за '/blog/./' ???
    IGNORED = ['/admin', '/edit', '/static', '/upload', '/blog/./']
    INDEX_PRIORITY = 1.0
    # LOGGER = sm_log


def create_sitemap(app):
    sm = FlaskSitemap(app, 'https://kazakov.ru.net', orm='sqlalchemy', config_obj=SMConfig)
    sm.add_rule('/blog', Post, loc_attr='slug', lastmod_attr='created')
    sm.add_rule('/blog/tag', Tag, loc_attr='slug', priority=0.8)
    return sm
