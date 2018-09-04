from datetime import datetime

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


def spotify_check_status_code(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        if res.status_code == 401:
            # No token provided
            raise NoTokenError('SAM does not have a token to connect to Spotify with', res.status_code)
        elif res.status_code < 200 or res.status_code >= 300:
            raise SamException('Error during a POST to the Spotify API',
                               status_code=res.status_code,
                               payload=res.text)
        return res
    return decorated
