import aiohttp, datetime
from bs4 import BeautifulSoup
from config import region_dict, token_dict
from timeinmatch import time_in_match

async def time_spent_week(accountId: str) -> int:
    url = 'https://' + region_dict[region_dict['current']] + \
          '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + \
          accountId + '?api_key=' + token_dict['league']

    #print(url)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js_time = await r.json()

                #print(js_time)

                match_list = js_time['matches']

                game = 0
                within_week = True
                time_played = 0

                current_time = datetime.datetime.now()


                while game < 100 and within_week == True:

                    # Since League of Legends marks timestamps with milliseconds
                    # I have to divide it by 1000 to get it to seconds
                    game_time = datetime.datetime.fromtimestamp(
                        match_list[game]['timestamp']/1000)

                    time_difference = current_time - game_time

                    if time_difference.days <= 7:
                        time_played += await time_in_match(match_list[game]['gameId'])

                    else:
                        within_week = False


                    game += 1

                return time_played

            else:
                return -1
