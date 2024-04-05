import requests

class MangaClient:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url

    def _send_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    def search(self, source, query):
        endpoint = f"/manga/{source}/{query}"
        return self._send_request(endpoint)

    def get_manga_info(self, source, manga_id):
        endpoint = f"/manga/{source}/info/{manga_id}"
        return self._send_request(endpoint)

    def get_chapter_pages(self, source, chapter_id):
        endpoint = f"/manga/{source}/read/{chapter_id}"
        return self._send_request(endpoint)