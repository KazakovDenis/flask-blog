from pytest import mark


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


@mark.parametrize('url,status', [
    ('/', 200),
    ('/notes', 200),
    ('/blog/tag/projects/', 200),
    ('/login', 200),
    ('/logout', 302),
    ('/admin', 308),
])
def test_service_accessible(client, url, status):
    """Checks that server is running and returning expected status codes"""
    response = client.get(url)
    assert response.status_code == status


def t_create_note(client, credentials):
    """Checks that new note page is accessible"""
    login(client, *credentials)
    response = client.get('/blog/create/')
    assert response.status_code == 200
