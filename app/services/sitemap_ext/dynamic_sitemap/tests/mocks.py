from copy import copy
from datetime import datetime
from logging import getLogger

from .. import SitemapMeta


class FuncMock:
    """A class for creating function mocks for testing

        Creating a mock:
    >>> do_smth = FuncMock(True, 'do_smth')
    >>> do_smth, do_smth()
    (<"do_smth" function mock>, True)
    """
    def __init__(self, to_return=None, name=None):
        self.container = to_return
        self.name = f'"{name}" ' if name else ''

    def __call__(self, *args, **kwargs):
        return self.container

    def __repr__(self):
        return f'<{self.name}function mock>'


class Mock:
    """A class for creating object mocks for testing

        Create one object:
    >>> app = Mock('none_arg', false_arg=False, another_arg='value', empty_mock_arg=None, \
                    callable_arg=lambda: 'value', mock_name='App')
    >>> app
    <"App" mock>

        Create instances of an object:
    >>> app(mock_name='First instance'), app(mock_name='Second instance'), app(mock_name='Third instance')
    (<"First instance of App" mock>, <"Second instance of App" mock>, <"Third instance of App" mock>)
    """
    def __init__(self, *args, **kwargs):
        self.mock_name = kwargs.pop('mock_name', 'Unknown')

        for arg in args:
            arg = str(arg)
            assert arg.isidentifier(), f'Arg "{arg}" is not a valid identifier'
            setattr(self, arg, None)

        for key, value in kwargs.items():
            setattr(self, key, value) if value is not None else setattr(self, key, Mock(mock_name='Empty'))

    def __repr__(self):
        return f'<"{self.mock_name}" mock>'

    def __call__(self, **kwargs):
        """Creates an instance of a mock
        :param kwargs: keys-values to override
        """
        instance = copy(self)
        instance.mock_name = f"{kwargs.pop('mock_name', 'Instance')} of {self.mock_name}"
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance


class DefaultSitemap(SitemapMeta):
    def __init__(self, app, base_url: str, config_obj=None):
        super().__init__(app, base_url, config_obj)


record = Mock('slug', 'updated', 'priority')
rule = Mock(methods=['GET'], rule='/url')


class Model:
    query = Mock(all=lambda: [record(slug='first-slug'), record(slug='second-slug')])
    objects = Mock(all=lambda: [record(slug='first-slug'), record(slug='second-slug')])
    updated = datetime.now()


class FlaskApp:
    extensions = {'sqlalchemy': True, 'peewee': True}
    url_map = Mock(iter_rules=lambda: [rule(), rule(rule='/ign/<slug>'), rule(rule='/app/<int:page>')])
    logger = getLogger('Flask')
    template_folder = ['dynamic_sitemap', 'tmp']
