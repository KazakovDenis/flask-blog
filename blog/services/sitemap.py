from dynamic_sitemap import FlaskSitemap

from blog.config import DOMAIN, PATH
from blog.models import Post, Tag


__all__ = 'create_sitemap',


class SMConfig:
    DEBUG = False
    APP_ROOT = PATH
    FOLDER = ('static',)
    TEMPLATE_FOLDER = ('templates',)
    # todo: что за '/blog/./' ???
    IGNORED = ['/admin', '/edit', '/static', '/upload', '/blog/./']
    INDEX_PRIORITY = 1.0


def create_sitemap(app) -> FlaskSitemap:
    """Create an endpoint for a sitemap"""
    sm = FlaskSitemap(app, base_url=DOMAIN, orm='sqlalchemy', config_obj=SMConfig)
    sm.add_rule('/blog', Post, loc_attr='slug', lastmod_attr='created')
    sm.add_rule('/blog/tag', Tag, loc_attr='slug', priority=0.8)
    return sm
