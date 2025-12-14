import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler

class SpotifyAuth:
    def __init__(self, **kwargs):
        self.scope = kwargs.setdefault("scope", "playlist-modify-private")
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))
        self.cache = CacheFileHandler(".cache")

    def get_user_id(self):
        return self.sp.current_user()["id"]

    def set_up_auth(self):
        token = self.cache.get_cached_token()["access_token"]
        header = {"Authorization": f"Bearer {token}"}
        return header