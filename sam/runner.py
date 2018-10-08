import os
from random import choices
from string import ascii_uppercase, digits

from flask import Flask
from flask.json import jsonify

from .exceptions import SamError
from .routes import setup_routes


def create_app():
    app_ = Flask(__name__)
    app_.secret_key = os.environ.get('SECRET_KEY', ''.join(choices(ascii_uppercase + digits, k=12)))
    setup_routes(app_)

    @app_.errorhandler(SamError)
    def handle_invalid_data_format(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    return app_


def run_app(host='0.0.0.0', port=None, debug=False, **kwargs):
    port = port or int(os.environ.get('PORT', 5000))
    create_app().run(host=host, port=port, debug=debug, **kwargs)


app = create_app()
