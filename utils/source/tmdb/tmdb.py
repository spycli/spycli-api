import requests

class TMDbFetcher:
    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3"
        self.api_key = "bca6bf3a093b3dd1345b29ae3512ae93"
        self.headers = {"accept": "application/json"}

    def search_multi(self, query):
        url = f"{self.base_url}/search/multi?api_key={self.api_key}&query={query}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            results = {}
            for item in data["results"]:
                name_or_title = item.get('name') or item.get('title', 'Unknown')
                release_date = item.get('release_date') or item.get('first_air_date', 'Unknown')
                combined_name = f"{name_or_title} ({release_date}, {item['media_type']})"
                link = f"/{item['media_type']}/{item['id']}"
                results[combined_name] = link
            return results
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def get_seasons_episode_structure(self, media_type, media_id):
        url = f"{self.base_url}/{media_type}/{media_id}?api_key={self.api_key}"
        tmdb_id = f"{media_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            seasons_data = data.get('seasons', [])
            seasons_episode_structure = {}
            for season in seasons_data:
                if season['name'].lower() != 'specials' and season['episode_count'] > 0:
                    season_name = season['name']
                    episodes = [f'Episode {i+1}' for i in range(season['episode_count'])]
                    seasons_episode_structure[season_name] = episodes
            return seasons_episode_structure, tmdb_id
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")
