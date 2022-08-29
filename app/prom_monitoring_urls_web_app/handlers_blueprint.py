from flask import Blueprint, render_template, current_app, Response
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, Gauge, REGISTRY
from prom_monitoring_urls_web_app.utils import check_connectivity_with_socket, get_list_of_hosts_from_config, get_url_response_code_and_time

base_bp = Blueprint('base', __name__, url_prefix='/')

@base_bp.route('/')
def index():
    return render_template('index.html', config = current_app.config['data'])



# app health will simply check connectivity to the hosts of urls
@base_bp.route('/health')
def health():
    # getting the list of urls
    response_code = 200
    response_message = 'OK'
    hosts = get_list_of_hosts_from_config(current_app.config['data']['urls'])
    current_app.logger.info(hosts)
    for host in hosts:
        if not check_connectivity_with_socket(host['name'], host['port']):
            response_code = 503
            response_message = 'The following host ' + host['name'] + ' is not reachable over the port: ' + str(host['port'])
            current_app.logger.error('NO connection. Socket: {0}'.format(host['name']))
            break
    return response_message, response_code


@base_bp.route('/metrics')
def metrics():
    try: 
        for url in current_app.config['data']['urls']:
            res_code, res_time = get_url_response_code_and_time(url)
            current_app.config['metrics']['sample_external_url_up'].labels(url).set(1 if res_code == 200 else 0)
            current_app.config['metrics']['sample_external_url_response_ms'].labels(url).observe(res_time)
        CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    except Exception as e:
        current_app.logger.error('failed to calculate metrics')
        current_app.logger.error(str(e))
        return '503 - Failed to calculate metrics, please check logs', 503
