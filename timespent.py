import aiohttp
from bs4 import BeautifulSoup
from config import region_dict

async def time_spent(summoner_name: str) -> int:
    url = 'https://wol.gg/stats/' + region_dict['current'] + '/' + \
          summoner_name.replace(' ','+') + '/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:

                text = await r.read()

                content_html = BeautifulSoup(text.decode('utf-8'),
                                                   features='html.parser')

                minutes_str = str(content_html.find('div', id='time-minutes'))

                minute_start = minutes_str.index('<p>') + 3
                minute_end = minutes_str[minute_start:].index('<') + minute_start

                return int(minutes_str[minute_start:minute_end].replace(',',''))

            else:
                return -1
