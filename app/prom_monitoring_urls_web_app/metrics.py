from prometheus_client import Gauge, Summary, CollectorRegistry, REGISTRY, ProcessCollector

import requests

# avoiding the issue: https://github.com/rycus86/prometheus_flask_exporter/issues/17
def unregister_metrics():
    for collector, names in tuple(REGISTRY._collector_to_names.items()):
        if any(name.startswith('flask_') or
               name.startswith('sample_external_url')
               for name in names):

            REGISTRY.unregister(collector)

#a registering the metrics with Prometheus Collector Registry
def initialize_metrics(app):
    if app.config['TESTING'] == True:
       unregister_metrics()
    app.config['metrics'] = {}
    app.config['metrics']['sample_external_url_up'] = Gauge('sample_external_url_up', 'URL status based on response status code, 0 if response code not 200', ['url'])
    app.config['metrics']['sample_external_url_response_ms'] = Summary('sample_external_url_response_ms', 'URL sresponse time in ms', ['url'])