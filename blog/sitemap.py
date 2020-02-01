import os
from xml.etree import ElementTree as et
from app import app, db
from models import Post, Tag


"""URIs to be excluded from the site map"""
EXCLUSIONS = ('/admin', '/edit', '/static', '/logout', '/upload')
BASE_URL = 'https://kazakov.ru.net'
MODELS = {'/blog/': Post, }
          # '/blog/tag/': Tag}


class Sitemap:
    """A sitemap generator"""

    attrs = {'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
             'xmlns': "http://www.sitemaps.org/schemas/sitemap/0.9",
             'xsi:schemaLocation':
                 "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"}

    """All app URIs"""
    app_uri = [i.rule for i in list(app.url_map.iter_rules())]

    def __init__(self, folder='/blog/static/'):
        self.uris = self._exclude()
        self.filename = folder + 'my_sitemap.xml'

    def _exclude(self):
        """Excludes URIs in exclusions from app_uri"""
        public_uris = self.app_uri

        for item in EXCLUSIONS:
            public_uris = [uri for uri in public_uris if item not in uri]

        return public_uris

    def _replace_slug(self):
        """Replaces '/model/<slug>/...' in self.uris with real URIs"""
        finished = [BASE_URL]

        for uri in self.uris:

            if '<slug>' in uri:
                prefix, end = uri.split('<slug>')[0], uri.split('<slug>')[-1]
                model = MODELS.get(prefix)

                try:
                    records = model.query.all()
                    # slug_list = [(f'{BASE_URL}{prefix}{obj.slug}{end}', obj.created) for obj in records]
                    slug_list = [f'{BASE_URL}{prefix}{obj.slug}{end}' for obj in records]
                    finished.extend(slug_list)
                except:
                    pass
            else:
                finished.append(BASE_URL + uri)

        return finished

    def build(self):
        """Builds an XML file"""
        links = self._replace_slug()
        url_set = et.Element('urlset', self.attrs)
        sub = et.SubElement

        for link in links:
            url = sub(url_set, "url")
            loc, lastmod, priority = sub(url, "loc"), sub(url, "lastmod"), sub(url, "priority")

            loc.text = link
            lastmod.text = '2020-01-04T19:50:34+01:00'
            priority.text = '1.0'

        tree = et.ElementTree(url_set)
        tree.write(self.filename, xml_declaration=True, encoding='UTF-8')


if __name__ == '__main__':
    sitemap = Sitemap()
    # [print(i) for i in sitemap._replace_slug()]
    sitemap.build()

