from logging import getLogger

from werkzeug.utils import import_string


logger = getLogger(__name__)


def create_instance(data: dict):
    """Create instance from fixture data"""
    import_name = data.get('class')
    try:
        cls = import_string(import_name)
    except (ImportError, ModuleNotFoundError):
        logger.warning(f'Could not import: {import_name}')
        return None

    kwargs = data.get('kwargs', {})
    try:
        instance = cls(**kwargs)
    except Exception as e:
        instance = None
        logger.warning(
            f'Could not instantiate "{import_name}" with kwargs: "{kwargs}". '
            f'Original exception was: "{e}"'
        )

    return instance
