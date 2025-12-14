from scraper import Scraper
from spotify_config import SpotifyConfig

user_input = input("Which year do you want to travel to? Provide the data in YYYY-MM-DD format: ")

def main():
    scraper = Scraper(user_input, website_url="https://www.officialcharts.com/charts/singles-chart/")
    spot_config = SpotifyConfig(playlist_name="UK Flames", description="Hottest Tracks Currently of 2025")

    collected_info = scraper.collect_information()

    track_uris = spot_config.get_track_ids(collected_info)

    spot_config.create_playlist(track_uris)

if __name__ == "__main__":
    main()