from urllib.parse import urlsplit
import socket, requests, yaml

#load config file.
def parse_config_file(app):
        with open("config.yaml", "r") as stream:
            try:
                config = yaml.safe_load(stream)
                app.logger.info('loaded config:' + str(config))
            except yaml.YAMLError as exc:
                app.logger.error('Unable to load config file, make sure that config.yaml file exists!')
                exit(1)
            return config

# this function will return the hosts and its ports for urls to be montiorined, it will also ensure that urls with the same host details are not duplicated
def get_list_of_hosts_from_config(app):
    hosts = []
    for url in app.config['data']['urls']:
        parsed_url = urlsplit(url)
        host_details = {'name': parsed_url.hostname, 'port': 80 if parsed_url.port == None else parsed_url.port }
    if host_details not in hosts:
        hosts.append(host_details)
    return hosts

# check connectivity to host over defined port
def check_connectivity_with_socket(app, host, port):
    try:
        conn = socket.create_connection((host, port))
        conn.close()
        app.logger.info('OK. established connection. Socket: {0}'.format(host))
        return True
    except Exception as ex:
        app.logger.error('NO connection. Socket: {0}'.format(host))
    return False 

def get_url_response_code_and_time(url):
    r = requests.get(url)
    return r.status_code, r.elapsed.total_seconds()