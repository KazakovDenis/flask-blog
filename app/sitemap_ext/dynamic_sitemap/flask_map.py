# -*- coding: utf-8 -*-
"""
This module provides a tool to generate a Sitemap of an Flask application.

Basic example:

    from flask import Flask
    from sitemap_ext import FlaskSitemap

    app = Flask(__name__)
    sitemap = FlaskSitemap(app, 'https://mysite.com')
    sitemap.config.IGNORED.extend(['/edit', '/upload'])
    sitemap.config.FOLDER = ('..', 'static',)
    sitemap.add_rule('/app', Post, lastmod='created')
    sitemap.add_rule('/app/tag', Tag, priority=0.4)
    app.add_url_rule('/sitemap.xml', endpoint='sitemap', view_func=sitemap.view)

IGNORED has a priority over add_rule. Also you can set configurations from your class:

    sm_logger = logging.getLogger('sitemap')
    sm_logger.setLevel(30)

    class Config:
        FOLDER = ('public',)
        IGNORED = ['/admin', '/back-office', '/other-pages']
        ALTER_PRIORITY = 0.1
        LOGGER = sm_logger

    sitemap = FlaskSitemap(app, 'https://myshop.org', config_obj=Config)
    sitemap.add_rule('/goods', Product, slug='id', lastmod='updated')
    app.add_url_rule('/sitemap.xml', endpoint='sitemap', view_func=sitemap.view)

Moreover you can get a static file by using:
    sitemap.build_static()
"""
from .main import *


FlaskApp = TypeVar('FlaskApp')


class FlaskSitemap(SitemapMeta):
    """A sitemap generator for a Flask application. For usage see the module documentation"""

    def __init__(self, app: FlaskApp, base_url: str, config_obj=None, orm: str='sqlalchemy'):
        """Creates an instance of a Sitemap

        :param app: an instance of Flask application
        :param base_url: your base URL such as 'http://site.com'
        :param config_obj: a class with configurations
        :param orm: an ORM name used in project
        """
        super().__init__(app, base_url, config_obj, orm)
        assert self.app.extensions.get(orm), f'{orm} extension is not found'

        self.template_folder = self.config.TEMPLATE_FOLDER or self.app.template_folder
        self._copy_template(self.template_folder)
        self.log.info(f'Sitemap has been initialized')

    def get_logger(self):
        """Returns logger"""
        logger = self.config.LOGGER or self.app.logger.getChild('sitemap')
        if self.config.DEBUG:
            self.set_debug_level(logger)
        return logger

    def get_rules(self) -> iter:
        """Returns an iterator of URL rules"""
        rules = [rule_obj.rule for rule_obj in self.app.url_map.iter_rules() if 'GET' in rule_obj.methods]
        rules.sort(key=len)
        return iter(rules)

    def view(self):
        """Generates a response such as Flask views do"""
        from flask import make_response, render_template, request

        self._prepare_data()
        template = render_template('sitemap.xml', data=self.data)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        self.log.info(f'[{request.method}] Requested by {request.remote_addr}')
        return response
