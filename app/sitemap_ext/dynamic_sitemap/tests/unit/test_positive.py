from ..conf import *

now = datetime.now().strftime('%Y-%m-%dT%H')


# Config tests
def test_config_from_obj(config):
    """Tests configuration's setters and getters"""
    class Conf:
        TEST = True
        ALTER_PRIORITY = 0.4
    config.from_object(Conf)
    assert hasattr(config, 'TEST')
    assert config['ALTER_PRIORITY']


# Base object tests
def test_default_create_map(default_map, config):
    """Tests an instance creation"""
    assert isinstance(default_map.start, str)
    assert now in default_map.start


@pytest.mark.parametrize('priority', [0.5, 0.733, 1])
def test_default_add_rule(default_map, priority):
    """Tests a rule creation"""
    default_map.add_rule('/app', Model, priority=priority, lastmod='updated')
    model = default_map.models['/app']
    assert model[0] == Model
    assert isinstance(model[1], str)
    assert isinstance(model[2], str)
    assert isinstance(model[3], (float, int))


def test_get_dynamic_rules(default_map):
    """Tests that the method returns only dynamic rules"""
    for url in default_map.get_dynamic_rules():
        assert '<' in url


def test_default_get_logger(default_map, request):
    """Tests a logger creation and debug level setup"""
    def teardown():
        default_map.config.DEBUG = False
    request.addfinalizer(teardown)

    default_map.config.DEBUG = True
    default_map.get_logger()
    assert default_map.log.level == 10


def test_default_copy_template(default_map, request):
    """Tests a static file copying to source folder"""
    def teardown():
        default_map.config.DEBUG = False
    request.addfinalizer(teardown)

    default_map.config.DEBUG = True
    default_map._copy_template(template_folder)
    assert os.path.exists(template)


def test_default_exclude(default_map):
    """Tests that ignored urls was excluded"""
    default_map.config.IGNORED = ['/ign']
    default_map.rules = ['/', '/url', '/ign']
    for url in default_map._exclude():
        assert 'ign' not in url


def test_default_prepare_data(default_map):
    """Tests preparing data by pattern"""
    assert not default_map.data
    default_map.config.ALTER_PRIORITY = 0.3
    default_map._prepare_data()
    assert default_map.data[-1].loc
    assert default_map.data[-1].lastmod
    assert default_map.data[-1].priority == 0.3


@pytest.mark.parametrize('prefix', ['', '/', '/prefix', '/pr_e/f1x'])
@pytest.mark.parametrize('suffix', ['', '/', '/suffix'])
def test_default_replace_patterns(default_map, prefix, suffix):
    """Tests preparing data from dynamic rules by pattern """
    uri = '/<slug>'
    default_map.rules = ['/', '/url', '/ign', uri]
    default_map.add_rule(prefix, Model)
    slug = '/' + Model.query.all()[0].slug
    record = default_map._replace_patterns(uri, [prefix, suffix])[0]
    assert record.loc == f'{default_map.url}{prefix}{slug}{suffix}'
    assert hasattr(record, 'lastmod')
    assert hasattr(record, 'priority')


# FlaskSitemap tests
def test_flask_create_map(flask_map):
    """Tests an instance creation"""
    assert flask_map.query == 'model.query.all()'


def test_flask_build_static(flask_map):
    """Tests a static file creation"""
    path = os.path.join(os.path.abspath(''), 'dynamic_sitemap', 'tmp', 'static.xml')
    flask_map.add_rule('/app', Model, lastmod='created')
    flask_map.config.IGNORED = ['/ign']
    flask_map.build_static(path)
    assert os.path.exists(path)
