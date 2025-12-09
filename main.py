from bs4 import BeautifulSoup
import requests
from utils import LABEL
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler

WEB_URL = "https://www.billboard.com/charts/hot-100/"
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_id = sp.current_user()["id"]
cache = CacheFileHandler(".cache")
token = cache.get_cached_token()["access_token"]

playlist_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"

header = {
    "Authorization": f"Bearer {token}"
}

user_input = input("Which year do you want to travel to? Provide the data in YYYY-MM-DD format: ")

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}
response = requests.get(f"{WEB_URL}{user_input}", headers=headers)

contents = response.text

soup = BeautifulSoup(contents, "html.parser")

def get_artists():
    artist_list = []
    artists = soup.find_all(name="span", class_=LABEL)
    for elm in artists:
        artist = elm.get_text().strip()
        artist_list.append(artist)
    return artist_list

def get_tracks():
    track_list = []
    titles = soup.select("li ul li h3")
    for track in titles:
        track = track.get_text().strip()
        track_list.append(track)
    return track_list

def collect_information():
    collected = {k:v for k, v in zip(get_artists(), get_tracks())}
    return collected

info = collect_information()

def get_ids():
    final_ids = []
    for index, value in info.items():
        search_params = {
            "q": f"track:{value}, artist:{index}",
            "type": "track",
            "market": "ES",
            "limit": 1,
        }
        next_response = requests.get(url="https://api.spotify.com/v1/search", params=search_params, headers=header)
        if data := next_response.json()["tracks"]["items"]:
            for track in data:
                final_ids.append(track["id"])
    return final_ids

playlist_params = {
    "name": f"Billboard Top 100 {user_input}",
    "public": False
}

playlist_response = requests.post(url=playlist_endpoint, json=playlist_params, headers=header)
playlist_id = playlist_response.json()["id"]
adding_tracks_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

ids = get_ids()

def get_uris(the_ids):
    the_uris = []
    for track in the_ids:
        the_uris.append(f"spotify:track:{track}")
    return the_uris

uris = get_uris(ids)

add_items_params = {
    "playlist_id": playlist_id,
    "uris": uris
    }

playlist_insertion = requests.post(url=adding_tracks_endpoint, json=add_items_params, headers=header)
print(playlist_insertion.text)