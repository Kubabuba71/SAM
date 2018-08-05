import os

from requests_oauthlib import OAuth2Session as r_OAuth2Session


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class OAuth2Session:
    def __init__(self):
        self.spotify_client_id = os.environ.get('SPOTIFY_CLIENT_ID')
        self.spotify_client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
        self.spotify_base_authorization_url = os.environ.get('SPOTIFY_AUTHORIZATION_URL')
        self.spotify_redirect_uri = os.environ.get('SPOTIFY_REDIRECT_URI')
        self.spotify_current_song_redirect_uri = os.environ.get('SPOTIFY_CURRENT_SONG_REDIRECT_URI')
        self.spotify_scope = ['user-read-playback-state']
        self.spotify_token_url = 'https://accounts.spotify.com/api/token'
        self.oauth2_session = r_OAuth2Session(self.spotify_client_id,
                                              redirect_uri=self.spotify_redirect_uri,
                                              scope=self.spotify_scope,
                                              state='sam_state')
        self.token = None
        self.authorization_response = None

    @property
    def authorization_response(self):
        return self.__authorization_response

    @authorization_response.setter
    def authorization_response(self, value):
        self.__authorization_response = value

    def get(self, url):
        print('GET the following resource:', url)
        response = self.oauth2_session.get(url)
        return response

    def authorization_url(self):
        authorization_url, state = self.oauth2_session.authorization_url(self.spotify_base_authorization_url)
        return authorization_url, state

    def fetch_token(self, authorization_response):
        self.authorization_response = authorization_response
        self.token = self.oauth2_session.fetch_token(self.spotify_token_url,
                                                     authorization_response=self.authorization_response,
                                                     client_secret=self.spotify_client_secret)
