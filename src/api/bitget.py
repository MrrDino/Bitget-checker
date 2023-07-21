import json
import aiohttp
import asyncio

from .constants import URL


async def get_info(chain: str = 'zkSyncEra', coin_id: str = '3') -> bool:
    """Функция получения информации о депозите в сети"""

    find = None

    async with aiohttp.ClientSession() as session:
        while not find:
            response = await session.get(url=URL)
            data = await response.json()

            for item in data['data']:
                if item['coinId'] == coin_id:
                    info = item['chains']

                    for i in info:
                        if i['chain'] == chain:
                            deposit = json.loads(i['rechargeable'])
                            find = True

            await asyncio.sleep(3)

    return deposit

