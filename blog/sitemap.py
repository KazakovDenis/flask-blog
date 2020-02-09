from app import app, db
from models import Post, Tag
from sitemap_ext.sitemap_ext import Sitemap


class Config:

    FOLDER = ('static',)
    IGNORED = ['/static', '/admin', ]
    INDEX_PRIORITY = 1.0


sitemap = Sitemap(app, 'https://kazakov.ru.net', config_obj=Config)
sitemap.add_rule('/blog', Post, lastmod='created')
sitemap.add_rule('/blog/tag', Tag, priority=0.8)


if __name__ == '__main__':
    sitemap.build()
