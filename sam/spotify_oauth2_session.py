from requests_oauthlib import OAuth2Session

from .constants import (SPOTIFY_BASE_AUTHORIZATION_URL, SPOTIFY_CLIENT_ID,
                        SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI,
                        SPOTIFY_SCOPE, SPOTIFY_TOKEN_URL, SPOTIFY_WRAPPER_STR)
from .exceptions import NoTokenError, SamException
from .utils import log, now_str, spotify_check_status_code

oauth2_session = OAuth2Session(SPOTIFY_CLIENT_ID,
                               redirect_uri=SPOTIFY_REDIRECT_URI,
                               scope=SPOTIFY_SCOPE,
                               state='sam_state')
token = None
authorization_response = None


@spotify_check_status_code
def get(url, data=None, params=None, **kwargs):
    log(f'{now_str()}-DEBUG_SAM: GET {url}')
    res = oauth2_session.get(url, data=data, params=params, **kwargs)
    if res.status_code < 200 or res.status_code > 3000:
        if res.status_code == 401:
            # No token provided
            raise NoTokenError('SAM does not have a token to connect to Spotify with', res.status_code)
        else:
            raise SamException('Error during a POST to the Spotify API',
                               status_code=res.status_code,
                               payload=res.text)
    return res


@spotify_check_status_code
def post(url, data=None, params=None, **kwargs):
    log(f'{now_str()}-DEBUG_SAM: POST {url}')
    res = oauth2_session.post(url, data=data, params=params, **kwargs)
    return res


@spotify_check_status_code
def put(url, data=None, params=None, **kwargs):
    log(f'{now_str()}-DEBUG_SAM: PUT {url}')
    res = oauth2_session.put(url, data=data, params=params, **kwargs)
    return res


def authorization_url():
    authorization_url_, state = oauth2_session.authorization_url(SPOTIFY_BASE_AUTHORIZATION_URL)
    log(f'{now_str()}-DEBUG{SPOTIFY_WRAPPER_STR}: Generating Spotify Authorization URL: {authorization_url_}')
    return authorization_url_, state


def fetch_token(authorization_response_):
    log(f'{now_str()}-DEBUG{SPOTIFY_WRAPPER_STR}: Fetching new Spotify Token')
    global authorization_response
    global token
    authorization_response = authorization_response_
    token = oauth2_session.fetch_token(SPOTIFY_TOKEN_URL,
                                       authorization_response=authorization_response,
                                       client_secret=SPOTIFY_CLIENT_SECRET)
