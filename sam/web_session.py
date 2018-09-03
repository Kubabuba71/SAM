from cachecontrol import CacheControl
from requests import session

from .utils import log, now_str

web_session = session()
cached_session = CacheControl(web_session)


def get_json(url, params=None, data=None, **kwargs):
    # type: (str, Optional[dict[str]]) -> dict
    """
    GET json located at url

    :param url: the url that json should be retrieve from
    :param params: optional parameters that can be used as URL parameters
    :param data: optional data that can be used as body_data
    :returns: dict that contains the json from the url location
    """
    r = get(url, params=params, data=data, **kwargs)
    return r.json()


def get(url, params=None, data=None, json_=None, **kwargs):
    """
    GET resource located at url

    :param url: the url that the GET request should be sent to
    :param params: optional parameters that can be used as URL parameters
    :param data: optional data that can be used as body_data
    :return: requests.Response
    """
    log(f'{now_str()}-DEBUG_SAM: GET {url}')
    r = cached_session.get(url, params=params, data=data, **kwargs)
    return r


def post(url, params=None, data=None, json=None, **kwargs):
    """
    POST to resource located at url

    :param url: the url that the POST request should be sent to
    :param params: optional parameters that can be used as URL parameters
    :param data: optional data that can be used as body_data
    :return: requests.Response
    """
    log(f'{now_str()}-DEBUG_SAM: POST {url}')
    r = cached_session.post(url, params=params, data=data, json=json, **kwargs)
    return r
