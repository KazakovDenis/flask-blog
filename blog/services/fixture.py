import json
from logging import getLogger
from pathlib import Path
from typing import Any, List, Union, Type

from werkzeug.utils import import_string


logger = getLogger(__name__)


def create_instance(data: dict):
    """Create instance from fixture data"""
    import_name = data.get('class')
    if not import_name:
        logger.warning('"class" key not found')
        return None

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


class Loader:
    """Loaders base class"""

    def __init__(self, path: Union[str, Path]):
        self.path = path

    def load(self) -> List[dict]:
        """Load fixtures data from the file"""
        raise NotImplementedError


class JSONLoader(Loader):

    def load(self) -> List[dict]:
        """Load fixtures data from the file"""
        path = check_path(self.path)

        with open(path) as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise TypeError(f'Fixtures in "{path}" need to put in list')

        return data


def get_loader_cls(fmt: str) -> Type[Loader]:
    """Get fixture source loader type"""
    if fmt == 'json':
        loader = JSONLoader
    else:
        raise NotImplementedError(f'The loader from {fmt} is not implemented yet.')

    return loader


def load_fixtures(*paths: Union[str, Path], fmt: str = 'json') -> list:
    """Load fixtures from a file"""
    loader_cls = get_loader_cls(fmt)

    instances = []
    for path in paths:
        loader = loader_cls(path)
        data = loader.load()

        for i in data:
            obj = create_instance(i)
            instances.append(obj)

    return instances
