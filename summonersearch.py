import aiohttp, json
from config import token_dict, region_dict
from champid import champ_id
from masterysearch import mastery_search
from rankedsearch import ranked_search
from timespent import time_spent
from timespentweek import time_spent_week

async def summoner_search(name:str):
    summoner_url = 'https://' + region_dict[region_dict['current']].lower() \
                   + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' \
                   + name + '?api_key=' + token_dict['league']

    async with aiohttp.ClientSession() as session:
        async with session.get(summoner_url) as r:
            if r.status == 200:
                js_summoner = await r.json()

                js_summoner['champ_mastery'] = await mastery_search(
                    js_summoner['id'], 5)

                js_summoner['ranked'] = await ranked_search(js_summoner['id'])

                js_summoner['time'] = await time_spent(name)

                js_summoner['time_week'] = await time_spent_week(js_summoner['accountId'])

                return js_summoner

            else:
                return {}
