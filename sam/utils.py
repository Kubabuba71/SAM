from datetime import datetime

from requests import Response

from .exceptions import NoTokenError, SamException

log = print


def logged(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        print(f'{now_str()}-DEBUG_RES: {res}')
        return res
    return decorated


def parse_action(action: str):
    action_components = action.split('.')
    if len(action_components) == 1:
        return action_components[0], None, None

    elif len(action_components) == 2:
        return action_components[0], action_components[1],  None

    elif len(action_components) == 3:
        return action_components[0], action_components[1], action_components[2]


def normalize_volume_value(volume):
    if isinstance(volume, str):
        volume = int(volume.strip().replace('%', ''))
    return volume


def now_str():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')


def verify_status_code(func):
    def decorated(*args, **kwargs) -> Response:
        res = func(*args, **kwargs)
        if res.status_code == 401:
            # No token provided
            raise NoTokenError('SAM does not have a token to connect to Spotify with', res.status_code)
        elif res.status_code < 200 or res.status_code >= 300:
            raise SamException(f'Error during a {res.request.method} to {res.request.url}',
                               status_code=res.status_code,
                               payload=res.text)
        return res
    return decorated


def log_url(func):
    def decorated(*args, **kwargs) -> Response:
        res = func(*args, **kwargs)
        url = res.url
        method = res.request.method
        log(f'{now_str()}-DEBUG_SAM: {method} {url}')
        return res
    return decorated
