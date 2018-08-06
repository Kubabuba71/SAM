import os
import json

from flask import Flask, request, make_response
from flask.json import jsonify

from sam.requesthandlers import RequestHandler
import sam.spotify_api_wrapper as spotify_api_wrapper
from sam.music import music

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


@app.route("/")
def hello():
    return "All is well and good with SAM!\n"


@app.route('/run_sample/<sample>')
def run_sample(sample):
    try:
        json_path = 'sample_dialogflow_requests/{}.json'.format(sample)
        with open(json_path) as raw_json_data:
            sample_dialogflow_request = json.load(raw_json_data)
        request_handler = RequestHandler(sample_dialogflow_request)
        json_res = request_handler.handle_request()
        res = make_response(json.dumps(json_res))
        res.headers['Content-Type'] = 'application/json'
        return res
    except IOError as e:
        return make_response(e)


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
    cwd = os.getcwd()
    requests_dir = os.path.join(cwd, 'sample_dialogflow_requests')
    for file in os.listdir(requests_dir):
        with open(os.path.join(requests_dir, file)) as raw_json_data:
            sample_request_data = json.load(raw_json_data)
            request_handler = RequestHandler(sample_request_data)
            response = request_handler.handle_request()
            response['purpose'] = sample_request_data['purposeShort']
            response['date'] = sample_request_data['queryResult']['parameters'].get('date', None)
            response['date-time'] = sample_request_data['queryResult']['parameters'].get('date-time', None)
            responses[file] = response
    res = make_response(json.dumps(responses))
    res.headers['Content-Type'] = 'application/json'
    return res


@app.route("/login")
def login():
    """
    Generic authorization request for the Spotify API
    """
    # authorization_url, state = oauth2_session.authorization_url()
    # print('Authorization URL: {}'.format(authorization_url))
    spotify_api_wrapper.login()
    return 'authorization_url printed to console, go to it'


@app.route("/spotify_callback")
def callback():
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


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    # When running locally, run on port 5000
    # When running on heroku (or a similar service), run on the provided port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
