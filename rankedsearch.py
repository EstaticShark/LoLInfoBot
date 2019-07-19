import aiohttp
from config import region_dict, token_dict

async def ranked_search(summoner_id: str) -> dict:
    summoner_url = 'https://' + region_dict[region_dict['current']].lower() + \
                   '.api.riotgames.com/lol/league/v4/entries/by-summoner/' \
                   + summoner_id + '?api_key=' + token_dict['league']

    async with aiohttp.ClientSession() as session:
        async with session.get(summoner_url) as r:
            if r.status == 200:
                js_champ = await r.json()

                return js_champ

            else:
                return {}