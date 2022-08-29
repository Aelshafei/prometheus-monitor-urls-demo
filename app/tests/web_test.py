import pytest
from prom_monitoring_urls_web_app import create_app

@pytest.fixture()
def app():
    app = create_app(test_config={'TESTING': True})
    yield app

@pytest.fixture()
def invalid_url_app():
    invalid_url_app = create_app(test_config={'TESTING': True})
    invalid_url_app.config['data']['urls'] = ['http://not.valid.url.com']
    yield invalid_url_app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def invalid_url_client(invalid_url_app):
    return invalid_url_app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def invalid_url_runner(invalid_url_app):
    return invalid_url_app.test_cli_runner()


def test_index(client):
    response = client.get('/')
    assert '<h1>Prometheus metrics for URLs availability and response availiability</h1>' in str(response.data)


def test_metrics(client):
    response = client.get('/metrics')
    assert 'python_gc_objects_collected_total' in str(response.data)

def test_health(client):
    response = client.get('/health')
    assert 'OK' in str(response.data)


def test_metrics_invalid_url(invalid_url_client):
    response = invalid_url_client.get('/metrics')
    assert '503' in str(response.data)

def test_health_invalid_url(invalid_url_client):
    response = invalid_url_client.get('/health')
    assert 'The following host ' in str(response.data)