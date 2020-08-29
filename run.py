import asyncio

import longpoll
import api

token = '33d406d998f9fca0565db1727f05badfb26f17f05275382870a64166c6e0cfe0088d6997b6e1963c30f86'
group_id = 179848057

def run():
    loop = asyncio.get_event_loop()

    lp = longpoll.LongpollBot(token, group_id)

    

    loop.run_until_complete(test_request())

async def test_request():
    vk = api.API(token, group_id).get_api()
    await vk.messages.send(text='текст', user_ids=[1,2,3])
    await vk.messages.send(text='testaatsad')

if __name__ == "__main__":
    run()