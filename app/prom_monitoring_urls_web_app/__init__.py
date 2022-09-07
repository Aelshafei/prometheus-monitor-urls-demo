from flask import Flask
import logging
from prom_monitoring_urls_web_app.utils import parse_config_file
from prom_monitoring_urls_web_app import handlers_blueprint
from prom_monitoring_urls_web_app.metrics import initialize_metrics



def create_app(test_config=None):
    app = Flask(__name__)

    # adding flask logs to gunicorn logging
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
   
    app.config['data'] = parse_config_file(app, 'config.yaml')


    # loading test config
    if test_config:
        app.config.update(test_config)

    initialize_metrics(app)
    
    app.register_blueprint(handlers_blueprint.base_bp)



    return app