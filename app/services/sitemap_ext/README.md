# Dynamic sitemap
[![Build Status](https://travis-ci.com/KazakovDenis/dynamic-sitemap.svg?branch=master)](https://travis-ci.com/KazakovDenis/dynamic-sitemap)  

A simple sitemap generator for Python projects.

Already implemented:
- Flask

Basic example:
```python
from flask import Flask
from dynamic_sitemap import FlaskSitemap

app = Flask(__name__)
sitemap = FlaskSitemap(app, 'https://mysite.com')
sitemap.config.IGNORED.extend(['/edit', '/upload'])
sitemap.config.TEMPLATE_FOLDER = ['app', 'templates']
sitemap.add_rule('/app', Post, lastmod='created')
sitemap.add_rule('/app/tag', Tag, priority=0.4)
app.add_url_rule('/sitemap.xml', endpoint='sitemap', view_func=sitemap.view)
```
*IGNORED* has a priority over *add_rule*.  
  
Also you can set configurations from your class (and __it's preferred__):
```python
sm_logger = logging.getLogger('sitemap')
sm_logger.setLevel(30)

class Config:
    TEMPLATE_FOLDER = ['app', 'templates']
    IGNORED = ['/admin', '/back-office', '/other-pages']
    ALTER_PRIORITY = 0.1
    LOGGER = sm_logger

sitemap = FlaskSitemap(app, 'https://myshop.org', config_obj=Config)
sitemap.add_rule('/goods', Product, slug='id', lastmod='updated')
app.add_url_rule('/sitemap.xml', endpoint='sitemap', view_func=sitemap.view)
```
Moreover you can get a static file by using:
```python
sitemap.build_static()
```