from scraper import Scraper
from spotify_config import SpotifyConfig

user_input = input("Which year do you want to travel to? Provide the data in YYYY-MM-DD format: ")

def main():
    scraper = Scraper(user_input)
    spot_config = SpotifyConfig()

    collected_info = scraper.collect_information()

    track_uris = spot_config.get_track_ids(collected_info)

    spot_config.create_playlist(track_uris, user_input)

if __name__ == "__main__":
    main()