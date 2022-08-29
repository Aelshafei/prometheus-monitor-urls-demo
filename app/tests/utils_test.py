import pytest
from prom_monitoring_urls_web_app import create_app
from prom_monitoring_urls_web_app.utils import check_connectivity_with_socket, get_list_of_hosts_from_config, parse_config_file
from prom_monitoring_urls_web_app.metrics import initialize_metrics

def test_load_config_valid():
    app = create_app(test_config={'TESTING': True})
    parse_config_file(app, "config.yaml")
    assert app.config['data']
    
def test_load_config_invalid_file():
    app = create_app(test_config={'TESTING': True})
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        parse_config_file(app, "configg.yaml")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_load_config_invalid_yaml():
    app = create_app(test_config={'TESTING': True})
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        parse_config_file(app, "./tests/invalid_config.yaml")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def initialize_metrics():
    app = create_app(test_config={'TESTING': True})
    initialize_metrics(app)
    assert app.config['dmetrics']

def test_check_connectivity_with_socket():
    assert check_connectivity_with_socket("google.com", 80)

def test_get_list_of_hosts_from_config():
    assert get_list_of_hosts_from_config(["https://httpstat.us/200","https://httpstat.us/503"]) == [{"name":"httpstat.us", "port":443}]