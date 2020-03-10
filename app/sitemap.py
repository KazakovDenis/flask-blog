from .blog import app
from .models import Post, Tag
from .services import FlaskSitemap, sm_log


class SMConfig:
    DEBUG = False
    FOLDER = ('static',)
    IGNORED = ['/admin', '/edit', '/static', '/upload']
    INDEX_PRIORITY = 1.0
    LOGGER = sm_log


sitemap = FlaskSitemap(app, 'https://kazakov.ru.net', config_obj=SMConfig)
sitemap.add_rule('/blog', Post, lastmod='created')
sitemap.add_rule('/blog/tag', Tag, priority=0.8)
sm_view = sitemap.view


if __name__ == '__main__':
    sitemap.build_static()
