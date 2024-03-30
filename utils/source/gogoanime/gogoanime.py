import requests

class GogoAnimeClient:
    def __init__(self, base_url="http://localhost:8787"):
        self.base_url = base_url

    def _send_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    def search_anime(self, search_term):
        search_term_encoded = requests.utils.quote(search_term)
        endpoint = f"/search/{search_term_encoded}"
        return self._send_request(endpoint)

    def get_anime_details(self, anime_id):
        endpoint = f"/anime/{anime_id}"
        return self._send_request(endpoint)

    def get_episode_stream_urls(self, episode_id):
        endpoint = f"/episode/{episode_id}"
        return self._send_request(endpoint)

    def get_episode_download_urls(self, episode_id):
        endpoint = f"/download/{episode_id}"
        return self._send_request(endpoint)

    def get_home(self):
        endpoint = "/home"
        return self._send_request(endpoint)
