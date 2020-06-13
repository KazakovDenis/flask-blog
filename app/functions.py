import re
from transliterate import translit
from uuid import uuid4


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
