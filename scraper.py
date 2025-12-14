from bs4 import BeautifulSoup
import requests
from utils import USER_AGENT

class Scraper:
    def __init__(self, user_input, **kwargs):
        self.user_input = user_input
        self.website_url = kwargs.setdefault("website_url", "https://www.billboard.com/charts/hot-100/")
        self.web_headers = kwargs.setdefault("web_headers", USER_AGENT)

    def scrape_website(self):
        response = requests.get(f"{self.website_url}{self.user_input}", headers=self.web_headers)
        contents = response.text
        soup = BeautifulSoup(contents, "html.parser")
        return soup

    def get_artists(self):
        soup = self.scrape_website()
        artist_list = []
        artists = soup.find_all(name="a", class_="chart-artist text-lg inline-block")
        for elm in artists:
            artist = elm.get_text().strip()
            artist_list.append(artist.lower())
        return artist_list

    def get_tracks(self):
        soup = self.scrape_website()
        track_list = []
        titles = soup.find_all(name="a", class_="chart-name font-bold inline-block")
        for track in titles:
            track = track.get_text().replace("RE", "").strip()
            clean_track = track.split("New")
            if clean_track[0] != "":
                track_list.append(clean_track[0].lower())
            else:
                track_list.append(clean_track[1].lower())
        return track_list

    def collect_information(self):
        collected = {k: v for k, v in zip(self.get_artists(), self.get_tracks())}
        return collected