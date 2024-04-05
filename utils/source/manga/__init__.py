import requests

class MangaClient:
    def __init__(self, base_url="https://consumet-seven-smoky.vercel.app"):
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


manga_client = MangaClient()
search_response = manga_client.search("mangadex", "demon")
print(search_response)
info_response = manga_client.get_manga_info("mangadex", "259dfd8a-f06a-4825-8fa6-a2dcd7274230")
print(info_response)
chapter_pages_response = manga_client.get_chapter_pages("mangadex", "5f7891b4-f048-4516-9c75-7bcd6dbd1451")
print(chapter_pages_response)
