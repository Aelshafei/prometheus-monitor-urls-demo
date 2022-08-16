from prometheus_client import Gauge, Summary
import requests


def initialize_metrics(app):
    app.config['metrics'] = {}
    app.config['metrics']['sample_external_url_up'] = Gauge('sample_external_url_up', 'URL status based on response status code, 0 if response code not 200', ['url'])
    app.config['metrics']['sample_external_url_response_ms'] = Summary('sample_external_url_response_ms', 'URL sresponse time in ms', ['url'])