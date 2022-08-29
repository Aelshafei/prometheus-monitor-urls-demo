from urllib.parse import urlsplit
import socket, requests, yaml

#load config file.
def parse_config_file(app, path='config.yaml'):
        try:
            with open(path, "r") as stream:
                try:
                    config = yaml.safe_load(stream)
                    app.logger.info('loaded config:' + str(config))
                except yaml.YAMLError as exc:
                    app.logger.error('Unable to load config file, make sure that config.yaml format is valid!')
                    exit(2)
                return config
        except Exception as e:
            app.logger.error('Unable to load config file, make sure that config.yaml file exists!')
            exit(1)

# this function will return the hosts and its ports for urls to be montiorined, it will also ensure that urls with the same host details are not duplicated
def get_list_of_hosts_from_config(urls):
    hosts = []
    for url in urls:
        parsed_url = urlsplit(url)
        if parsed_url.scheme == 'https':
            default_port = 443
        else:
            default_port = 80
        host_details = {'name': parsed_url.hostname, 'port': default_port if parsed_url.port == None else parsed_url.port }
    if host_details not in hosts:
        hosts.append(host_details)
    return hosts

# check connectivity to host over defined port
def check_connectivity_with_socket(host, port):
    try:
        conn = socket.create_connection((host, port))
        conn.close()
        return True
    except Exception as ex:
        return False 

def get_url_response_code_and_time(url):
    r = requests.get(url)
    return r.status_code, r.elapsed.total_seconds()