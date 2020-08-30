import asyncio

import aiohttp

class API():
    API_URL = 'https://api.vk.com/method'

    def __init__(self, token: str, group_id: int, v: str = '5.122',):
        self.token = token
        self.group_id = group_id
        self.v = v

        self.session = aiohttp.ClientSession()
        self.loop = asyncio.get_event_loop()

    
    async def method(self, method, data = None):
        print(method)
        print(data)
        data['access_token'] = self.token
        data['group_id'] = self.group_id
        data['v'] = self.v

        response = await self.session.post(f'{self.API_URL}/{method}', data=data)
        result = await response.json()
        print(result)
        return result['response']

    def get_api(self):
        return APIMethod(self)

    async def close(self):
        self.session.close()


class APIMethod():
    def __init__(self, vk: API, method: str = None):
        self._vk = vk
        self._method = method

    def __getattr__(self, method: str):
        if '_' in method:
            m = method.split('_')
            method = m[0].join(w.title() for w in m[1:])
        
        return APIMethod(self._vk, (self._method + '.' if self._method else '') + method)
    
    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, (list, tuple)):
                kwargs[key] = ','.join(str(x) for x in value)

        return self._vk.loop.create_task(self._vk.method(self._method, kwargs))

