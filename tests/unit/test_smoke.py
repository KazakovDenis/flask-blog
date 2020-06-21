from pytest import mark
from requests import get as http_get

from tests.conf import *


urls_to_test = [
    (BASE_URL, 200),
    (BASE_URL + '/---', 404),
]


@mark.parametrize('url', urls_to_test)
def test_service_running(url):
    """Checks that server is running and returning expected status codes"""
    response = http_get(url[0])
    assert response.status_code == url[1]
