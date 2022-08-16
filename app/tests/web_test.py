import pytest
from prom_monitoring_urls_web_app import create_app
from prometheus_client import CollectorRegistry, REGISTRY

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_index(client):
    response = client.get('/')
    assert '<h1>Prometheus metrics for URLs availability and response availiability</h1>' in str(response.data)


def test_metrics(client):
    response = client.get('/metrics')
    assert 'python_gc_objects_collected_total' in str(response.data)