from ..conf import *


@pytest.mark.parametrize('priority', [5, -1, '0.5', 'high'])
def test_priority_01(flask_map, priority):
    """Assertion error should be raised when priority is not in range 0.0-1.0.
    TypeError should be raised when got non-numeric."""
    with pytest.raises((AssertionError, TypeError)):
        flask_map.add_rule('/app', Model, priority=priority)


def test_default_copy_exception(default_map, request):
    """Tests exception which should be raised when sitemap.xml already exists (it's created when Sitemap initializes)
     and DEBUG set False"""
    def teardown():
        default_map.config.DEBUG = True
    request.addfinalizer(teardown)

    default_map.config.DEBUG = False
    with pytest.raises(FileExistsError):
        default_map._copy_template(template_folder)
