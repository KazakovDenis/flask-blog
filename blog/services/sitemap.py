import os

from flask import Flask
from dynamic_sitemap import FlaskSitemap

from blog import config
from blog.models import Post, Tag


__all__ = 'create_sitemap',


class SMConfig:
    DEBUG = False
    APP_ROOT = config.APP_ROOT
    FOLDER = str(config.STATIC_DIR)
    TEMPLATE_FOLDER = str(config.TEMPLATES_DIR)
    # todo: что за '/blog/./' ???
    IGNORED = ['/admin', '/edit', '/static', '/upload', '/blog/./']
    INDEX_PRIORITY = 1.0


def create_sitemap(app: Flask, domain: str) -> FlaskSitemap:
    """Create an endpoint for a sitemap"""
    # todo: убрать после устранения в dynamic-sitemap
    os.makedirs(SMConfig.TEMPLATE_FOLDER, exist_ok=True)
    if not domain.startswith('http'):
        domain = f'https://{domain}'

    sm = FlaskSitemap(app, base_url=domain, orm='sqlalchemy', config_obj=SMConfig)
    sm.add_rule('/blog', Post, loc_attr='slug', lastmod_attr='created')
    sm.add_rule('/blog/tag', Tag, loc_attr='slug', priority=0.8)
    return sm
