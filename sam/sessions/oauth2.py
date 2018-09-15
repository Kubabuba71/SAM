from requests_oauthlib import OAuth2Session as OAuth2Session_

from ..utils import log, log_url, now_str, verify_status_code


class Session:
    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 redirect_uri=None,
                 token_uri=None,
                 authorization_uri=None,
                 scope=None,
                 state='sam_state',
                 component=None
                 ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_uri = token_uri
        self.authorization_uri = authorization_uri
        self.scope = scope
        self.state = state
        self.component = component

        self._session = OAuth2Session_(self.client_id,
                                       redirect_uri=self.redirect_uri,
                                       scope=self.scope,
                                       state=self.state)
        self.token = None
        self.authorization_response = None

    @verify_status_code
    @log_url
    def get(self, url, data=None, params=None, **kwargs):
        return self._session.get(url, data=data, params=params, **kwargs)

    @verify_status_code
    @log_url
    def post(self, url, data=None, params=None, **kwargs):
        return self._session.post(url, data=data, params=params, **kwargs)

    @verify_status_code
    @log_url
    def put(self, url, data=None, params=None, **kwargs):
        return self._session.put(url, data=data, params=params, **kwargs)

    def authorization_url(self):
        authorization_url_, state = self._session.authorization_url(self.authorization_uri)
        log(f'{now_str()}-DEBUG{self.state}: Generating {self.component} Authorization URL: {authorization_url_}')
        return authorization_url_, state

    def fetch_token(self, authorization_response_):
        log(f'{now_str()}-DEBUG{self.state}: Fetching new {self.component} Token')
        self.authorization_response = authorization_response_
        self.token = self._session.fetch_token(self.token_uri,
                                               authorization_response=self.authorization_response,
                                               client_secret=self.client_secret)
