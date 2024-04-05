import requests

class DramaCoolClient:
    def __init__(self, base_url="http://localhost:3000/movies/dramacool"):
        self.base_url = base_url

    def _send_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    def search(self, query, page=1):
        endpoint = f"/{query}"
        return self._send_request(endpoint, params={"page": page})

    def get_info(self, drama_id):
        endpoint = "/info"
        return self._send_request(endpoint, params={"id": drama_id})

    def get_streaming_links(self, episode_id, media_id, server="asianload"):
        endpoint = "/watch"
        return self._send_request(endpoint, params={"episodeId": episode_id, "mediaId": media_id, "server": server})