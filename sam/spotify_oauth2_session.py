from requests_oauthlib import OAuth2Session

from .constants import (SPOTIFY_BASE_AUTHORIZATION_URL, SPOTIFY_CLIENT_ID,
                        SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI,
                        SPOTIFY_SCOPE, SPOTIFY_TOKEN_URL)

oauth2_session = OAuth2Session(SPOTIFY_CLIENT_ID,
                               redirect_uri=SPOTIFY_REDIRECT_URI,
                               scope=SPOTIFY_SCOPE,
                               state='sam_state')
token = None
authorization_response = None


def get(url, params=None):
    print('GET the following resource:', url)
    if params is not None:
        res = oauth2_session.get(url, params=params)
    else:
        res = oauth2_session.get(url)
    return res


def post(url, params=None):
    print('POST the following resource:', url)
    if params is not None:
        res = oauth2_session.post(url, params=params)
    else:
        res = oauth2_session.post(url)
    return res


def put(url, data=None):
    print('PUT the following resource: ', url)
    if data is not None:
        res = oauth2_session.put(url, data=data)
    else:
        res = oauth2_session.put(url)
    return res


def authorization_url():
    print('Generating Spotify Authorization URL')
    authorization_url_, state = oauth2_session.authorization_url(SPOTIFY_BASE_AUTHORIZATION_URL)
    print('Authorization URL: {}'.format(authorization_url_))
    return authorization_url_, state


def fetch_token(authorization_response_):
    print('Fetching New Spotify Token')
    global authorization_response
    global token
    authorization_response = authorization_response_
    token = oauth2_session.fetch_token(SPOTIFY_TOKEN_URL,
                                       authorization_response=authorization_response,
                                       client_secret=SPOTIFY_CLIENT_SECRET)
