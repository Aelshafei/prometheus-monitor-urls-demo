from flask import Flask
import socket
from prom_monitoring_urls_web_app.utils import parse_config_file
from prom_monitoring_urls_web_app import handlers_blueprint
from prom_monitoring_urls_web_app.metrics import initialize_metrics



def create_app(test_config=None):
    app = Flask(__name__)
   
    app.config['data'] = parse_config_file(app)

    if test_config:
        app.config.update({
            'TESTING': True
        })

    initialize_metrics(app)
    
    app.register_blueprint(handlers_blueprint.base_bp)



    return app