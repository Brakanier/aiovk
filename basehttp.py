import aiohttp

class BaseHTTP():
    API_URL = 'https://api.vk.com/method'

    def __init__(self):
        self.session = aiohttp.ClientSession()

