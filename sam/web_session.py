from requests import session
from cachecontrol import CacheControl

web_session = session()
cached_session = CacheControl(web_session)


def get_json(url, params=None):
    # type: (str, Optional[dict[str]]) -> dict
    """
    GET json located at url

    :param url: the url that json should be retrieve from
    :param params: optional parameters that can be used as URL parameters
    :returns: dict that contains the json from the url location
    """
    r = get(url, params=params)
    return r.json()


def get(url, params=None):
    """
    GET resource located at url

    :param url: the url that the GET request should be sent to
    :param params: optional parameters that can be used as URL parameters
    :return: requests.Response
    """
    if params is None:
        r = cached_session.get(url)
    else:
        r = cached_session.get(url, params=params)
    return r


def post(url, params=None):
    """
    POST to resource located at url

    :param url: the url that the POST request should be sent to
    :param params: optional parameters that can be used as URL parameters
    :return: requests.Response
    """
    r = cached_session.post(url, params=params)
    return r
