import aiohttp
from config import region_dict, token_dict

async def mastery_search(summoner_id: str, top_num: int) -> dict:
    summoner_url = 'https://' + region_dict[region_dict['current']].lower() \
                   + '.api.riotgames.com/lol/champion-mastery/v4/' \
                     'champion-masteries/by-summoner/' + summoner_id + \
                   '?api_key=' + token_dict['league']

    async with aiohttp.ClientSession() as session:
        async with session.get(summoner_url) as r:
            if r.status == 200:
                js_champ = await r.json()

                return js_champ[:top_num]

            else:
                return []