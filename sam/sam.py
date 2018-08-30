import json
import os
from random import choices
from string import ascii_uppercase, digits

from flask import Flask, make_response, redirect, request, send_file
from flask.json import jsonify

from sam import spotify_api_wrapper
from sam.constants import (SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY,
                           STATIC_FILES_DIRECTORY)
from sam.music import music
from sam.requesthandlers import RequestHandler

from .dialogflow_api_wrapper import make_query

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', ''.join(choices(ascii_uppercase + digits, k=12)))
app.workers = 1


@app.route("/")
def hello():
    file_path = os.path.abspath(os.path.join(STATIC_FILES_DIRECTORY, 'sam-text.html'))
    return send_file(file_path)
    # return "All is well and good with SAM!\n"


@app.route('/run_sample/<sample>')
def run_sample(sample):
    try:
        json_file = f'{sample}.json'
        json_path = os.path.abspath(os.path.join(SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY, json_file))
        with open(json_path) as raw_json_data:
            sample_dialogflow_request = json.load(raw_json_data)
        request_handler = RequestHandler(sample_dialogflow_request)
        json_res = request_handler.handle_request()
        res = make_response(json.dumps(json_res))
        res.headers['Content-Type'] = 'application/json'
        return res
    except FileNotFoundError as e:
        return make_response(str(e))


@app.route("/dialogflow_webhook", methods=['POST'])
def dialogflow_webhook():
    """
    Handle requests from dialogflow
    """
    req = request.get_json(silent=True, force=True)
    request_handler = RequestHandler(req)
    json_res = json.dumps(request_handler.handle_request())
    res = make_response(json_res)
    res.headers['Content-Type'] = 'application/json'
    return res


@app.route('/test_all')
def test_all():
    """
    Test all requests, found in the folder sample_dialogflow_requests
    """
    responses = {}
    for file in os.listdir(SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY):
        with open(os.path.join(SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY, file)) as raw_json_data:
            sample_request_data = json.load(raw_json_data)
            response = RequestHandler(sample_request_data).handle_request()
            response['purpose'] = sample_request_data['purposeShort']
            responses[file] = response
    return jsonify(responses)


@app.route("/login")
def login():
    """
    Generic authorization request for the Spotify API
    """
    authorization_url = spotify_api_wrapper.login()
    return redirect(authorization_url)


@app.route("/spotify_callback")
def spotify_callback():
    """
    Generic authorization callback for the Spotify API
    """
    spotify_api_wrapper.callback(request.url)
    return 'Token has been fetched and saved'


@app.route("/current_song")
def current_song():
    """
    Return current Spotify playback information
    """
    res = spotify_api_wrapper.currently_playing()
    return jsonify(res.json())


@app.route('/get_token_info')
def get_token_info():
    res = spotify_api_wrapper.token_info()
    return jsonify(res)


@app.route('/current_song_info')
def current_song_info():
    res = music()
    return res


@app.route('/static/<filename>')
def static_file(filename):
    file_path = os.path.abspath(os.path.join(STATIC_FILES_DIRECTORY, filename))
    return send_file(file_path)


@app.route('/query', methods=['GET'])
def query():
    res = make_query(request.headers['query'])
    return res['result']['fulfillment']['speech']


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    # When running locally, run on port 5000
    # When running on heroku (or a similar service), run on the provided port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
