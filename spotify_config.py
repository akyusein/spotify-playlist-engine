import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler

class SpotifyConfig:
    def __init__(self, **kwargs):
        self.scope = kwargs.setdefault("scope", "playlist-modify-private")
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))
        self.user_id = self.sp.current_user()["id"]
        self.cache = CacheFileHandler(".cache")
        self.playlist_endpoint = kwargs.setdefault("playlist_endpoint", f"https://api.spotify.com/v1/users/{self.user_id}/playlists")
        self.search_endpoint = kwargs.setdefault("search_endpoint", "https://api.spotify.com/v1/search")

    def set_up_auth(self):
        token = self.cache.get_cached_token()["access_token"]
        header = {"Authorization": f"Bearer {token}"}
        return header

    def get_track_ids(self, collected_info):
        track_uris = []
        for index, value in collected_info.items():
            search_params = {
                "q": f"track:{value}, artist:{index}",
                "type": "track",
                "market": "ES",
                "limit": 1,
            }
            next_response = requests.get(url=self.search_endpoint, params=search_params, headers=self.set_up_auth())
            if data := next_response.json()["tracks"]["items"]:
                for track in data:
                    track_uris.append(f'spotify:track:{track["id"]}')
        return track_uris

    def create_playlist(self, uris, user_input):
        playlist_params = {
            "name": f"Billboard Top 100 {user_input}",
            "description": "Billboard Top 100 Songs For This Date!",
            "public": False
        }

        playlist_response = requests.post(url=self.playlist_endpoint, json=playlist_params, headers=self.set_up_auth())
        playlist_id = playlist_response.json()["id"]
        adding_tracks_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        add_items_params = {
            "playlist_id": playlist_id,
            "uris": uris
        }

        try:
            requests.post(url=adding_tracks_endpoint, json=add_items_params, headers=self.set_up_auth())
        except KeyError:
            print("Wrong parameters parsed in the API request")
        else:
            print("The playlist has been created and modified!")