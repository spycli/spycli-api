import requests

class TorrentClient:
    def __init__(self, base_url="http://localhost:8009"):
        self.base_url = base_url

    def _send_request(self, endpoint, params=None):
        """Utility method to send requests to the server."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    def search_on_site(self, site, query, limit=None, page=1):
        """Search for torrents on a specific site."""
        endpoint = "/api/v1/search"
        params = {'site': site, 'query': query, 'limit': limit, 'page': page}
        return self._send_request(endpoint, params=params)

    def search_all_sites(self, query, limit=None):
        """Search for torrents across all sites."""
        endpoint = "/api/v1/all/search"
        params = {'query': query, 'limit': limit}
        return self._send_request(endpoint, params=params)
