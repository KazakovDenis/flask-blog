from app import app, db
from models import Post, Tag
from sitemap_ext import Sitemap


sitemap = Sitemap(app, 'https://kazakov.ru.net')
sitemap.config.IGNORED.extend(['/logout', '/upload'])
sitemap.config.FOLDER = ('static',)
sitemap.add_rule('/blog', Post, updated='created')
sitemap.add_rule('/blog/tag', Tag, priority=0.8)


if __name__ == '__main__':
    sitemap.build()
