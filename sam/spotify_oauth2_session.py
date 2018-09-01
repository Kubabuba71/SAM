from datetime import datetime

from requests_oauthlib import OAuth2Session

from .constants import (SPOTIFY_BASE_AUTHORIZATION_URL, SPOTIFY_CLIENT_ID,
                        SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI,
                        SPOTIFY_SCOPE, SPOTIFY_TOKEN_URL)
from .exceptions import NoTokenError
from .utils import log

oauth2_session = OAuth2Session(SPOTIFY_CLIENT_ID,
                               redirect_uri=SPOTIFY_REDIRECT_URI,
                               scope=SPOTIFY_SCOPE,
                               state='sam_state')
token = None
authorization_response = None


def get(url, data=None, params=None, **kwargs):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    log(f'DEBUG-{now}: SAM->GET {url}')
    res = oauth2_session.get(url, data=data, params=params, **kwargs)
    if res.status_code == 401:
        # No token provided
        raise NoTokenError('SAM does not have a token to connect to Spotify with')
    return res


def post(url, data=None, params=None, **kwargs):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    log(f'DEBUG-{now}: SAM->POST {url}')
    res = oauth2_session.post(url, data=data, params=params, **kwargs)
    if res.status_code == 401:
        # No token provided
        raise NoTokenError('SAM does not have a token to connect to Spotify with')
    return res


def put(url, data=None, params=None, **kwargs):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    log(f'DEBUG-{now}: SAM->PUT {url}')
    res = oauth2_session.put(url, data=data, params=params, **kwargs)
    if res.status_code == 401:
        # No token provided
        raise NoTokenError('SAM does not have a token to connect to Spotify with')
    return res


def authorization_url():
    authorization_url_, state = oauth2_session.authorization_url(SPOTIFY_BASE_AUTHORIZATION_URL)
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    log(f'DEBUG-{now}: Generating Spotify Authorization URL: {authorization_url_}')
    return authorization_url_, state


def fetch_token(authorization_response_):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    log(f'DEBUG-{now}: Fetching new Spotify Token')
    global authorization_response
    global token
    authorization_response = authorization_response_
    token = oauth2_session.fetch_token(SPOTIFY_TOKEN_URL,
                                       authorization_response=authorization_response,
                                       client_secret=SPOTIFY_CLIENT_SECRET)
