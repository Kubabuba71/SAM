import json
import os
from random import choices
from string import ascii_uppercase, digits

from flask import Flask, make_response, redirect, request, send_file
from flask.json import jsonify

from . import spotify_api_wrapper
from .constants import (SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY,
                        STATIC_FILES_DIRECTORY)
from .dialogflow_api_wrapper import make_query
from .exceptions import SamException
from .music import current_song, music_action
from .requesthandlers import handle_sam_request
from .weather import weather_action

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', ''.join(choices(ascii_uppercase + digits, k=12)))
app.workers = 1


@app.errorhandler(SamException)
def handle_invalid_data_format(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/", methods=['GET'])
def hello_get_endpoint():
    file_path = os.path.abspath(os.path.join(STATIC_FILES_DIRECTORY, 'sam-text.html'))
    return send_file(file_path)


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


@app.route('/test_all', methods=['GET'])
def test_all_get_endpoint():
    """
    Test all requests, found in the folder sample_dialogflow_requests
    """
    responses = {}
    for file in os.listdir(SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY):
        with open(os.path.join(SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY, file)) as raw_json_data:
            sample_request_data = json.load(raw_json_data)
        response = handle_sam_request(sample_request_data)
        response['purpose'] = sample_request_data['purposeShort']
        responses[file] = response
    return jsonify(responses)


@app.route("/login", methods=['GET'])
def login_get_endpoint():
    """
    Generic authorization request for the Spotify API
    """
    authorization_url = spotify_api_wrapper.login()
    return redirect(authorization_url)


@app.route("/spotify_callback", methods=['GET'])
def spotify_callback_get_endpoint():
    """
    Generic authorization callback for the Spotify API
    """
    spotify_api_wrapper.callback(request.url)
    return 'Token has been fetched and saved'


@app.route("/current_song_json", methods=['GET'])
def current_song_json_get_endpoint():
    """
    Return current Spotify playback information
    """
    res = spotify_api_wrapper.currently_playing().json()
    return jsonify(res)


@app.route('/spotify_token_info', methods=['GET'])
def spotify_token_info_get_endpoint():
    res = spotify_api_wrapper.token_info()
    return jsonify(res)


@app.route('/current_song', methods=['GET'])
def current_song_get_endpoint():
    res = current_song()
    return res


@app.route('/static/<filename>', methods=['GET'])
def static_file_get_endpoint(filename):
    file_path = os.path.abspath(os.path.join(STATIC_FILES_DIRECTORY, filename))
    return send_file(file_path)


@app.route('/query', methods=['POST'])
def query_post_endpoint():
    res = make_query(request.get_json().get('query'))
    return res['result']['fulfillment']['speech']


@app.route('/music', methods=['GET'])
def music_get_endpoint():
    res = current_song()
    return res


@app.route('/music', methods=['POST'])
def music_post_endpoint():
    json_data = request.get_json(silent=True, force=True)
    res = music_action(json_data)
    return jsonify({
        'fulfillmentText': res
    })


@app.route('/calendar', methods=['GET'])
def calendar_get_endpoint():
    return jsonify({
        'fulfillmentText': 'Not Implemented Yet'
    })


@app.route('/calendar', methods=['POST'])
def calendar_post_endpoint():
    return jsonify({
        'fulfillmentText': 'Not Implemented Yet'
    })


@app.route('/weather', methods=['GET'])
def weather_get_endpoint():
    return jsonify({
        'fulfillmentText': 'Not Implemented Yet'
    })


@app.route('/weather', methods=['POST'])
def weather_post_endpoint():
    json_data = request.get_json(silent=True, force=True)
    res = weather_action(json_data)
    return jsonify({
        'fulfillmentText': res
    })


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    # When running locally, run on port 5000
    # When running on heroku (or a similar service), run on the provided port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
