import asyncio

import aiohttp


class LongpollBot():
    API_URL = 'https://api.vk.com/method'

    def __init__(self, token: str, group_id: int, v: str = '5.122'):
        self.group_id = group_id
        self.token = token
        self.v = v

        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()

        self._server = None
        self._key = None
        self._ts = None
        self._wait = 25
        
        
    
    async def get_longpoll_session(self):
        params = {
            'group_id': self.group_id,
            'access_token': self.token,
            'v': self.v
        }
        response = await self.session.get(f'{self.API_URL}/groups.getLongPollServer', params=params)
        data = await response.json()
        print(data)
        self._server = data['response']['server']
        self._ts = data['response']['ts']
        self._key = data['response']['key']
        

    async def run(self):
        if not self._key or not self._ts or self._wait:
            await self.get_longpoll_session()
        
        while True:
            print('start_updates')
            for e in await self.updates():
                self.loop.create_task(self.reply(e, 'Ответ'))
            
    async def updates(self):
        params = {
            'act': 'a_check',
            'key': self._key,
            'ts': self._ts,
            'wait': self._wait
        }
        response = await self.session.get(f'{self._server}', params=params)
        print(response.status)
        
        data = await response.json()
        print(data)
        self._ts = data['ts']
        return data['updates']


    async def reply(self, e: dict, text: str):
        data = {
            'peer_id': e['object']['message']['peer_id'],
            'random_id': 0,
            'message': text,
            'group_id': self.group_id,
            'access_token': self.token,
            'v': self.v
        }
        await asyncio.sleep(3)
        response = await self.session.post(f'{self.API_URL}/messages.send', data=data)
        result = await response.json()
        print(result)
        
        print('answered')
