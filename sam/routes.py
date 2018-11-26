import json
import os

from flask import make_response, redirect, request, send_file
from flask.json import jsonify

from .constants import (SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY,
                        STATIC_FILES_DIRECTORY)
from .requesthandlers import handle_sam_request
from .utils import Timer
from .wrappers import calendar_, dialogflow, spotify


def setup_routes(app):
    setup_dialogflow_endpoints(app)
    setup_calendar_endpoints(app)
    setup_music_endpoints(app)
    setup_weather_endpoints(app)
    setup_sample_endpoints(app)
    setup_static_endpoints(app)
    return app


def setup_dialogflow_endpoints(app):
    @app.route("/dialogflow_webhook", methods=['POST'])
    def dialogflow_webhook_post_endpoint():
        """
        Handle requests from dialogflow
        """
        json_data = request.get_json(silent=True, force=True)
        res = handle_sam_request(json_data)
        return jsonify({
            'fulfillmentText': res
        })

    @app.route('/query', methods=['POST'])
    def query_post_endpoint():
        res = dialogflow.make_query(request.get_json().get('query'))
        return res['result']['fulfillment']['speech']

    return app


def setup_calendar_endpoints(app):
    """
    Setup all the endpoints related to calendar functionality
    """
    @app.route('/calendar_login', methods=['GET'])
    def calendar_login_get_endpoint():
        """
        Generic authorization request for the Google Calendar API
        """
        authorization_url = calendar_.oauth2.authorization_url()
        return redirect(authorization_url)

    @app.route('/calendar_callback', methods=['GET'])
    def calendar_callback_get_endpoint():
        """
        Generic authorization callback for the Google Calendar API
        """
        calendar_.oauth2.fetch_token(request.url)
        return 'Google Calendar Token has been fetched and saved'

    @app.route('/calendar_events', methods=['GET'])
    def calender_events_get_endpoint():
        """
        Get upcoming events
        """
        res = calendar_.get_events()
        return jsonify(res)

    return app


def setup_music_endpoints(app):
    """
    Setup all the endpoints related to music functionality
    """
    @app.route("/spotify_login", methods=['GET'])
    def login_get_endpoint():
        """
        Generic authorization request for the Spotify API
        """
        authorization_url = spotify.oauth2.authorization_url()
        return redirect(authorization_url)

    @app.route("/spotify_callback", methods=['GET'])
    def spotify_callback_get_endpoint():
        """
        Generic authorization callback for the Spotify API
        """
        spotify.oauth2.fetch_token(request.url)
        return 'Spotify Token has been fetched and saved'

    @app.route("/current_song", methods=['GET'])
    def current_song_json_get_endpoint():
        """
        Return current Spotify playback information
        """
        res = spotify.currently_playing().json()
        return jsonify(res)

    @app.route('/spotify_token_info', methods=['GET'])
    def spotify_token_info_get_endpoint():
        res = spotify.token_info()
        return jsonify(res)

    return app


def setup_weather_endpoints(app):
    return app


def setup_sample_endpoints(app):
    """
    Setup all the endpoints related to running sample requests & tests
    """
    @app.route('/run_sample/<sample>', methods=['GET'])
    def run_sample_get_endpoint(sample):
        try:
            json_file = f'{sample}.json'
            json_path = os.path.abspath(
                os.path.join(
                    SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY, json_file
                )
            )

            with open(json_path) as file_:
                sample_dialogflow_request = json.load(file_)

            res = handle_sam_request(sample_dialogflow_request)
            return jsonify(res)
        except FileNotFoundError as e:
            return make_response(str(e))

    @app.route('/test_all', methods=['GET'])
    def test_all_get_endpoint():
        """
        Test all requests, found in the folder sample_dialogflow_requests
        """
        with Timer() as timer:
            responses = dict()
            responses['items'] = []
            for file in os.listdir(SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY):
                with open(os.path.join(SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY, file)) as raw_json_data:
                    sample_request_data = json.load(raw_json_data)
                response = handle_sam_request(sample_request_data)
                if isinstance(response, str):
                    response = {
                        'response': response
                    }
                response['purpose'] = sample_request_data['purposeShort']
                responses['items'].append(response)
        responses['responseTime'] = timer.response_time()
        return jsonify(responses)

    return app


def setup_static_endpoints(app):
    """
    Setup all the endpoints related to serving static files
    """
    @app.route("/", methods=['GET'])
    def hello_get_endpoint():
        # file_path = os.path.abspath(os.path.join(STATIC_FILES_DIRECTORY, 'sam-text.html'))
        # return send_file(file_path)
        return 'Hello world 🙃'

    @app.route('/bd', methods=['GET'])
    def bd():
        file_path = os.path.abspath(os.path.join(STATIC_FILE_DIRECTORY, 'index.html'))
        return send_file(file_path)

    @app.route('/static/<filename>', methods=['GET'])
    def static_file_get_endpoint(filename):
        file_path = os.path.abspath(os.path.join(STATIC_FILES_DIRECTORY, filename))
        return send_file(file_path)

    @app.route('/smile', methods=['GET'])
    def smile():
        return 'Just smile 😊'

    @app.route('/bday', methods=['GET'])
    def bday():
        return 'Happy birthday 😊'

    return app
