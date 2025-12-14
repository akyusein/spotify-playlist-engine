import requests
from spotify_auth import SpotifyAuth

class SpotifyConfig:
    def __init__(self, playlist_name, description, **kwargs):
        self.playlist_name = playlist_name
        self.description = description
        self.auth = SpotifyAuth().set_up_auth()
        self.user_id = kwargs.setdefault("user_id", SpotifyAuth().get_user_id())
        self.playlist_endpoint = kwargs.setdefault("playlist_endpoint", f"https://api.spotify.com/v1/users/{self.user_id}/playlists")
        self.search_endpoint = kwargs.setdefault("search_endpoint", "https://api.spotify.com/v1/search")

    def get_track_ids(self, collected_info):
        track_uris = []
        for index, value in collected_info.items():
            search_params = {
                "q": f"{index} {value}",
                "type": "track",
                "market": "ES",
                "limit": 1,
                "offset": 0
            }
            next_response = requests.get(url=self.search_endpoint, params=search_params, headers=self.auth)
            if data := next_response.json()["tracks"]["items"]:
                for track in data:
                    track_uris.append(track["uri"])
        return track_uris

    def create_playlist(self, uris):
        playlist_params = {
            "name": self.playlist_name,
            "description": self.description,
            "public": False
        }

        playlist_response = requests.post(url=self.playlist_endpoint, json=playlist_params, headers=self.auth)
        playlist_id = playlist_response.json()["id"]
        adding_tracks_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        add_items_params = {
            "playlist_id": playlist_id,
            "uris": uris
        }

        try:
            requests.post(url=adding_tracks_endpoint, json=add_items_params, headers=self.auth)
        except KeyError:
            print("Wrong parameters parsed in the API request")
        else:
            print("The playlist has been created and modified.")