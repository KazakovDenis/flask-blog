import logging
import os
import re
from uuid import uuid4

from transliterate import translit

from app import config


def configure_logger(app) -> logging.Logger:
    """Configure an app logger"""
    for name in ('flask', 'gunicorn'):
        folder = os.path.join(config.LOG_DIR, name)
        os.makedirs(folder, exist_ok=True)

    logger = app.logger
    logger.setLevel(config.LOG_LEVEL)
    fh = logging.FileHandler(os.path.join(config.LOG_DIR, 'flask', 'app.log'), encoding='utf-8')
    fh.setLevel(config.LOG_LEVEL)
    fh.setFormatter(logging.Formatter(config.LOG_FORMAT))
    logger.addHandler(fh)
    return logger


def rusify(txt: str) -> str:
    """Turns given text from Cyrillic symbols to Latin"""
    pattern = r'[^\w{IsCyrillic}]'
    txt += ' '                         # it may not work for clean Cyrillic
    if re.search(pattern, txt):
        txt = translit(txt, 'ru', reversed=True)
    return txt


def slugify(txt: str) -> str:
    """Makes text adapted for URL"""
    if txt is None:
        return str(uuid4())
    txt = rusify(txt.lower())
    pattern = r'[^a-z0-9]+'            # replaces all special symbols with dashes
    slug = re.sub(pattern, '-', txt)
    return slug.strip('-')
