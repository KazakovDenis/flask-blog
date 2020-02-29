# -*- coding: utf-8 -*-
"""
This module provides a tool to generate a Sitemap of an application.

Already implemented:
- Flask

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
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from datetime import datetime
from itertools import tee
from os.path import abspath, join, exists
from re import split
from typing import TypeVar
from xml.etree import ElementTree as ET

from flask import render_template, make_response, request


# todo: lastmod неизменённых
# todo: решить с path:path, path:filename в replace patterns # /static/<path:filename>
# todo: тесты

__all__ = ('Record', 'SitemapMeta', 'FlaskSitemap', 'DjangoSitemap')

Record = namedtuple('Record', 'loc lastmod priority')
Response = TypeVar('Response')
FlaskApp = TypeVar('FlaskApp')
DjangoApp = TypeVar('DjangoApp')


class SitemapConfig:
    """A class to set configurations

    DEBUG - if True sets up logging to DEBUG level
    FOLDER - NOT NEED FOR DYNAMIC SITEMAP, a tuple of folders to make path where to put a STATIC sitemap.xml,
    TEMPLATE_FOLDER - where to put a template for a dynamic sitemap, a tuple of folders
    IGNORED - a list of strings which ignored URIs contain
    INDEX_PRIORITY - float, a priority of the index page
    CONTENT_PRIORITY - float, a priority of pages generated by models
    ALTER_PRIORITY - float, a priority of other pages
    LOGGER - an instance of logging.Logger, creates child of app.logger if not set
    """

    DEBUG = False
    FOLDER = ('..', )
    TEMPLATE_FOLDER = None
    IGNORED = ['/admin', '/static', ]
    INDEX_PRIORITY = CONTENT_PRIORITY = ALTER_PRIORITY = None
    LOGGER = None

    def from_object(self, obj):
        """Updates the values from the given object
        :param obj: a class with the same attributes as this one
        """
        if obj:
            for key in dir(obj):
                if key.isupper():
                    self[key] = getattr(obj, key)

        return self

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        return self.__dict__.get(item)

    def __repr__(self):
        return '<Sitemap configurations object>'


class SitemapMeta(metaclass=ABCMeta):
    """The base class to inherit"""

    urlset_attrs = (
        'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        'xsi:schemaLocation='
        '"http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"'
    )

    attrs = dict([i.replace('"', '').split('=') for i in urlset_attrs])

    tree = f"""<?xml version='1.0' encoding='UTF-8'?>
                <urlset {' '.join(urlset_attrs)}>
                    {'{% for record in data %}'}
                        <url>
                            <loc>{'{{ record.loc }}'}</loc>
                            {'{% if record.lastmod %}'}
                                <lastmod>{'{{ record.lastmod }}'}</lastmod>
                            {'{% endif %}'}
                            {'{% if record.priority %}'}
                                <priority>{'{{ record.priority }}'}</priority>
                            {'{% endif %}'}
                        </url>
                    {'{% endfor %}'}
                </urlset>
            """

    queries = {
        'flask': 'model.query.all()',
        'django': 'model.objects.all()',
    }

    @abstractmethod
    def __init__(self, app, base_url: str, config_obj=None):
        """Creates an instance of a Sitemap

        :param app: an application instance
        :param base_url: your base URL such as 'http://site.com'
        :param config_obj: a class with configurations
        """
        self.config = SitemapConfig().from_object(config_obj)
        self.start = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.app = app
        self.url = base_url

        # attributes to override
        self.log = self.config.LOGGER     # an instance of logging.Logger (set in config)
        self.rules = None                 # a list of URL rules of an app like ['/model/<slug>', '/<path:path>']
        self.query = None                 # a query to get all objects of a model: self.queries[framework_name]

        # containers
        self.data = []                    # to store Record instances
        self.models = {}                  # to store db objects added by add_rule

    def add_rule(self, path: str, model, slug='slug', lastmod: str=None, priority: float=None):
        """Adds a rule to the builder to generate urls by a template using models of an app

        :param path: a part of URI is used to get a page generated through a model
        :param model: a model of an app that has a slug, e.g. an instance of SQLAlchemy.Model
        :param slug: a slug attribute of this model
        :param lastmod: an attribute of this model which is instance of the datetime object
        :param priority: a priority of URL to be set
        """
        if priority:
            priority = round(priority or self.config.CONTENT_PRIORITY, 1)
            assert 0.0 < priority <= 1.0, 'Priority should be a float between 0.0 and 1.0'

        self.models.update({path: (model, slug, lastmod, priority)})

    def build_static(self, filename='sitemap.xml'):
        """Builds an XML file. The system user of the app should have rights to write files

        :param filename: the name of target file (without path)
        """
        self._prepare_data()

        fullname = join(*self.config.FOLDER, filename) if self.config.FOLDER else filename
        self.log.info(f'Creating {fullname}...')

        url_set = ET.Element('urlset', self.attrs)
        sub = ET.SubElement

        for record in self.data:
            url = sub(url_set, "url")
            sub(url, "loc").text = record.loc

            if record.lastmod:
                sub(url, "lastmod").text = record.lastmod

            if record.priority:
                sub(url, "priority").text = str(record.priority)

        tree = ET.ElementTree(url_set)
        try:
            tree.write(fullname, xml_declaration=True, encoding='UTF-8')
        except FileNotFoundError as e:
            error = f'Seems like {filename} is not found or credentials required.'
            self.log.error(error)
            raise Exception(error) from e

        self.log.info('Static sitemap is ready')

    def set_debug_level(self):
        """Sets up logger and its handlers levels to Debug"""
        self.log.setLevel(10)
        for handler in self.log.handlers:
            handler.setLevel(10)

    def view(self) -> Response:
        """Method to override.
        :returns http response
        """
        pass

    def _create_template(self, folder: str):
        """Creates an xml file with Jinja2 template in app templates directory
        :param folder: a template folder
        """
        root = abspath(self.app.__module__).rsplit('/', 1)[0]
        filename = ''.join((root, '/', folder, '/sitemap.xml'))

        if not exists(filename):
            try:
                with open(filename, 'w') as file:
                    file.write(self.tree)
                    self.log.info(f'Template has been created: {filename}')
            except FileNotFoundError as e:
                error = f'BAD PATH: Seems like {filename} is not found or credentials required.'
                self.log.error(error)
                raise Exception(error) from e

    def _exclude(self) -> iter:
        """Excludes URIs in config.IGNORED from self.rules"""
        self.rules, public_uris = tee(self.rules, 2)

        if self.config.DEBUG:
            public_uris = tuple(public_uris)
            self.log.debug(f'Rules before exclusion: {len(public_uris)}')

        for item in self.config.IGNORED:
            public_uris = iter([uri for uri in public_uris if item not in uri])

        if self.config.DEBUG:
            public_uris = tuple(public_uris)
            self.log.debug(f'Rules left: {len(public_uris)}')

        return public_uris

    def _prepare_data(self):
        """Prepares data to be used by builder"""
        self.data.clear()
        self.data.append(Record(self.url, self.start, self.config.INDEX_PRIORITY))
        uris = self._exclude()

        for uri in uris:
            self.log.debug(f'Preparing Records for {uri}')
            splitted = split(r'/<[\w:]+>', uri, maxsplit=1)

            if len(splitted) > 1:
                replaced = self._replace_patterns(uri, splitted)
                self.data.extend(replaced)
            else:
                self.data.append(Record(self.url + uri, self.start, self.config.ALTER_PRIORITY))

        self.log.debug('Data for the sitemap is ready')

    def _replace_patterns(self, uri: str, splitted: list) -> list:
        """Replaces '/<converter:name>/...' with real URIs

        :param uri: a relative URL without base
        :param splitted: a list with parts of URI
        :returns a list of Records
        """

        prefix, end = splitted[0], splitted[-1]
        prefix = '/' if not prefix else prefix

        assert self.models.get(prefix), f"Your should add '{uri}' or it's part to ignored or add a new rule"

        model, slug, updated, priority = self.models.get(prefix)
        prepared = []

        try:
            for record in eval(self.query):
                if slug:
                    uri = getattr(record, slug)
                    loc = f'{self.url}{prefix}/{uri}{end}'
                else:
                    loc = f'{self.url}{prefix}{end}'

                if updated:
                    lastmod = getattr(record, updated)
                    if isinstance(lastmod, datetime):
                        lastmod = lastmod.strftime('%Y-%m-%dT%H:%M:%S')
                else:
                    lastmod = None

                prepared.append(Record(loc, lastmod, priority))
        except AttributeError:
            self.log.warning(f'{model} has no attributes: {slug} and/or {updated}')

        self.log.debug(f'Included {len(prepared)} records')
        return prepared

    def __repr__(self):
        return f'<Sitemap object of {self.url} based on {self.app} >'


class FlaskSitemap(SitemapMeta):
    """A sitemap generator for a Flask application"""

    def __init__(self, app: FlaskApp, base_url: str, config_obj=None):
        """Creates an instance of a Sitemap

        :param app: an instance of Flask application
        :param base_url: your base URL such as 'http://site/com'
        :param config_obj: a class with configurations
        """
        super().__init__(app, base_url, config_obj)
        assert self.app.extensions.get('sqlalchemy'), 'Flask-SQLAlchemy not found'

        if not self.log:
            self.log = self.app.logger.getChild('sitemap')
        if self.config.DEBUG:
            self.set_debug_level()

        self.query = self.queries['flask']
        self.rules = [rule_obj.rule for rule_obj in self.app.url_map.iter_rules() if 'GET' in rule_obj.methods]
        self.rules.sort(key=len)
        self.rules = iter(self.rules)
        self.template_folder = self.config.TEMPLATE_FOLDER or self.app.template_folder

        self._create_template(self.template_folder)
        self.log.info(f'Sitemap has been initialized')

    def view(self):
        self._prepare_data()
        template = render_template('sitemap.xml', data=self.data)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        self.log.info(f'[{request.method}] Requested by {request.remote_addr}')
        return response