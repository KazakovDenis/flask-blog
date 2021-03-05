import json
from logging import getLogger
from pathlib import Path
from typing import Any, List, Union

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


def check_path(path: Any) -> Path:
    """Check path is correct"""
    if isinstance(path, str):
        path = Path(path)

    if not isinstance(path, Path):
        raise TypeError(f'Wrong file path "{path}", type: "{type(path)}"')

    if not path.exists():
        raise FileNotFoundError(f'No such fixture source: {path}')

    return path


def load_json(path: Union[str, Path]) -> List[dict]:
    """Load fixtures data from file"""
    path = check_path(path)

    with open(path) as file:
        data = json.load(file)
        if not isinstance(data, list):
            raise TypeError(f'Fixtures in "{path}" need to put in list')

    return data


def get_loader(fmt: str):
    """Get fixture source loader"""
    if fmt == 'json':
        loader = load_json
    else:
        raise NotImplementedError(f'The loader from {fmt} is not implemented yet.')

    return loader


def load_fixtures(*paths: Union[str, Path], fmt: str = 'json') -> list:
    """Load fixtures from a file"""
    loader = get_loader(fmt)

    instances = []
    for path in paths:
        data = loader(path)

        for i in data:
            obj = create_instance(i)
            instances.append(obj)

    return instances
