import os

import json

from flask import Flask, request, redirect, session, make_response
from flask.json import jsonify

from requests_oauthlib import OAuth2Session

from sam.requesthandlers import RequestHandler
from sam.weather import get_coordinates, get_offset_from_utc

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

spotify_client_id = os.environ.get('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
spotify_authorization_url = os.environ.get('SPOTIFY_AUTHORIZATION_URL')
spotify_redirect_uri = os.environ.get('SPOTIFY_REDIRECT_URI')
spotify_scope = ['user-read-playback-state']
spotify_token_url = 'https://accounts.spotify.com/api/token'


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
        res = make_response(json_res)
        res.headers['Content-Type'] = 'application/json'
        return res
    except IOError as e:
        return make_response(e)


@app.route("/dialogflow_webhook", methods=['POST'])
def webhook():
    """
    Handle requests from dialogflow
    """
    req = request.get_json(silent=True, force=True)
    request_handler = RequestHandler(req)
    res = request_handler.handle_request()
    res = make_response(json.dumps(res))
    res.headers['Content-Type'] = 'application/json'
    return res


@app.route('/test_location/<location>')
def test_something(location):
    """
    A random test for some functionality
    """
    coordinates = get_coordinates(location)
    offset = get_offset_from_utc(coordinates)
    result = {'location': location,
              'coords': coordinates,
              'offset': offset}
    res = make_response(json.dumps(result))
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
    spotify = OAuth2Session(spotify_client_id, redirect_uri=spotify_redirect_uri, scope=spotify_scope)
    authorization_url, state = spotify.authorization_url(spotify_authorization_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    """
    Generic authorization callback for the Spotify API
    """
    spotify_oauth2_session = OAuth2Session(spotify_client_id, state=session['oauth_state'],
                                           redirect_uri=spotify_redirect_uri, scope=spotify_scope)
    token = spotify_oauth2_session.fetch_token(spotify_token_url, client_secret=spotify_client_secret,
                                               authorization_response=request.url)

    return jsonify(spotify_oauth2_session.get('https://api.spotify.com/v1/me/player').json())


@app.route("/current_song")
def current_song():
    """
    Return current Spotify playback information
    """
    spotify_oauth2_session = OAuth2Session(spotify_client_id, redirect_uri=spotify_redirect_uri, scope=spotify_scope)
    authorization_url, state = spotify_oauth2_session.authorization_url(spotify_authorization_url)
    session['oauth_state'] = state
    print('Spotify Authorization URL:\n{}\n'.format(authorization_url))
    return redirect(authorization_url)


@app.route("/current_song_callback")
def current_song_callback():
    """
    Authorization callback for current Spotify playback information
    """
    spotify_oauth2_session = OAuth2Session(spotify_client_id, state=session['oauth_state'],
                                           redirect_uri=spotify_redirect_uri, scope=spotify_scope)
    token = spotify_oauth2_session.fetch_token(spotify_token_url, client_secret=spotify_client_secret,
                                               authorization_response=request.url)

    return jsonify(spotify_oauth2_session.get('https://api.spotify.com/v1/me/player/currently-playing').json())


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    # When running locally, run on port 5000
    # When running on heroku (or a similar service), run on the provided port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
