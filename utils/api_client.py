import httpx

class APIClient:
    """封裝 HTTP 請求的 client"""

    BASE_URL = "https://jsonplaceholder.typicode.com"
    def __init__(self, base_url):
        self.client = httpx.Client(base_url=base_url)

    def get(self, endpoint, **kwargs):
        return self.client.get(endpoint, **kwargs)
    def post(self, endpoint, **kwargs):
        return self.client.post(endpoint, **kwargs)
    def put(self, endpoint, **kwargs):
        return self.client.put(endpoint, **kwargs)
    def delete(self, endpoint, **kwargs):
        return self.client.delete(endpoint, **kwargs)
    
    def close(self):
        self.client.close()

    def set_auth_token(self, token: str):
        self.client.headers['Authorization'] = f"Bearer {token}"