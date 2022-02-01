import aiohttp
import asyncio
import base64

class GH_API():
    def __init__(self):
        self.conn = None
        self.headers = {}

        self.endpoint = 'https://api.github.com'

        self.method = "GET"
        self.url = "/"

        self.response = None

        self.add_header("User-Agent", "GitHub-Follower")

    def add_header(self, key, val):
        self.headers[key] = val

    def make_connection(self):
        self.conn = aiohttp.ClientSession()

    async def send_request(self):
        if self.method == "POST":
            self.response = await self.conn.post(self.endpoint + self.url, headers = self.headers)
        elif self.method == "PUT":
            self.response = await self.conn.put(self.endpoint + self.url, headers = self.headers)
        elif self.method == "DELETE":
            self.response = await self.conn.delete(self.endpoint + self.url, headers = self.headers)
        else:
            self.response = await self.conn.get(self.endpoint + self.url, headers = self.headers)

    async def retrieve_response(self):
        return await self.response.text()

    def authenticate(self, user, token):
        mix = user + ":" + token

        r = base64.b64encode(bytes(mix, encoding='utf8'))

        self.add_header("Authorization", "Basic " + r.decode('ascii'))

    async def send(self, method = "GET", url = "/", headers = None):
        # Make connection.
        self.make_connection()

        # Insert additional headers.
        if headers is not None:
            for k, v in headers:
                self.headers[k] = v

        # Make method and URL.
        self.method = method
        self.url = url

        # Send request.
        await self.send_request()

    async def close(self):
        await self.conn.close()