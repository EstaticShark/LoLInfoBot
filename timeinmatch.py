import aiohttp
from config import region_dict, token_dict


async def time_in_match(matchId: str) -> int:
    url = 'https://' + region_dict[region_dict['current']] + \
          '.api.riotgames.com/lol/match/v4/matches/' + \
          str(matchId) + '?api_key=' + token_dict['league']

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js_match_time = await r.json()

                return js_match_time['gameDuration']

            else:
                return -1
