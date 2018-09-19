from cachecontrol import CacheControl
from requests import Session

from ..utils import log_url


class WebSession:
    def __init__(self):
        self._session = CacheControl(Session())

    def get_json(self, url, params=None, data=None, **kwargs):
        # type: (str, Optional[dict[str]]) -> dict
        """
        GET json located at url
        """
        return self.get(url, params=params, data=data, **kwargs).json()

    @log_url
    def get(self, url, params=None, data=None, **kwargs):
        """
        GET resource located at url
        """
        return self._session.get(url, params=params, data=data, **kwargs)

    @log_url
    def post(self, url, params=None, data=None, json=None, **kwargs):
        """
        POST to resource located at url
        """
        return self._session.post(url, params=params, data=data, json=json, **kwargs)
