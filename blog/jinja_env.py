from logging import getLogger

from flask import Flask

from . import config


logger = getLogger(__name__)


def debug(value):
    logger.debug(f'[template] value={value} of type={type(value)}')


def get_parameters(value):
    """Jinja filter to get Parameters of the group"""
    if not isinstance(value, str):
        logger.error('The value in get_parameters is not a string!')

    result = config.parameters(group=value)
    if not result:
        return []

    return result


def set_jinja_env(app: Flask):
    """Set Jinja2 environment"""
    app.jinja_env.globals.update(
        # Common
        DOMAIN=config.DOMAIN,
        MAINTAINER=config.MAINTAINER,

        # Contacts
        GITHUB_USER=config.GITHUB_USER,
        CONTACT_EMAIL=config.CONTACT_EMAIL,
        CONTACT_TELEGRAM=config.CONTACT_TELEGRAM,

        # Integrations
        DISQUS_URL=config.DISQUS_URL,
        YANDEX_METRIKA_ID=config.YANDEX_METRIKA_ID,
        GOOGLE_ANALYTICS_ID=config.GOOGLE_ANALYTICS_ID,
    )

    app.jinja_env.filters['debug'] = debug
    app.jinja_env.filters['params_group'] = get_parameters
