import discord, aiohttp, json
from math import ceil
from champid import champ_id
from config import token_dict, region_dict
from summonersearch import summoner_search

"""
Comments about program:
    Below is the code for the discord bot and all the commands it can take.
    Originally I wanted to split everything up into methods but I will do that
    once I understand the decorators for the discord module
"""


client = discord.Client()

@client.event  # Event for when bot is ready
async def on_ready():
    print("LoL Info Tool is ready!")


@client.event
async def on_message(msg):
    if len(msg.content) > 0:


        # Welcome Message: Complete
        if msg.content.lower().startswith('!hello'):
            channel = msg.channel
            await channel.send('Hello, there summoner. I am ready to receive input. For a list of inputs, type: !help')


        # Help Message: Work in progress
        elif msg.content.lower().startswith('!help'):
            """ The following are the help messages
            !help: Menu of commands and inputs
            !hello: Welcome message
            !summoner <Summoner Name>: Returns info on given summoner, summoner name must not contain punctuation or accents
            !region <Region>: Changes the region the bot operates in. Changing the region affects everyone else using the bot in the server
            
            """
            channel = msg.channel
            help_msg = '!help: Menu of commands and inputs\n' \
                       '!hello: Welcome message\n' \
                       '!summoner <Summoner Name>: Returns info on given ' \
                       'summoner, summoner name must not contain punctuation ' \
                       'or accents (GOOD: BestMidNA, Nuclear Gandhi, etc. BAD: ' \
                       'IEat.Dimsum, Flip,And Dip, etc.)\n' \
                       '!region <Region>: Changes the region the bot operates ' \
                       'in. Changing the region affects everyone else using ' \
                       'the bot in the server (Region Codes: BR, EUNE, EUW, JP, ' \
                       'KR, LAN, LAS, NA, OCE, TR, RU, PBE) (NA is default)'

            embed = discord.Embed(title='Help',
                                  description='Menu of Commands and Inputs',
                                  color=0x0000ff)
            embed.add_field(name='Commands', value=help_msg, inline=False)

            embed.set_footer(text='Page 1/1')
            await channel.send(embed=embed)


        # Change Region: Complete
        elif msg.content.lower().startswith('!region'):
            channel = msg.channel

            new_code = msg.content.upper()[8:].strip(' ')

            if new_code in region_dict.keys():
                if new_code == region_dict['current']:
                    await channel.send('The tool is already set on ' + new_code)


                else:
                    region_dict['current'] = new_code
                    await channel.send('The tool is now set to ' +
                                       region_dict['current'] + ' on the url: '
                                       + region_dict[
                                           region_dict['current']].lower()
                                       + '.api.riotgames.com')
            else:
                await channel.send('The region code ' + new_code +
                                   ' does not exist')


        # Summoner Search: Work in progress
        elif msg.content.lower().startswith('!summoner'):
            '''Returns an embedded message with the summoner's name, summoner 
            id, level, icon, and top three champions by mastery
            '''
            channel = msg.channel
            valid_name = True
            name = msg.content[10:].strip()


            punc = ',./;\'[]<>?:\"{}!@#$%^&*()_+-='

            for item in punc:
                if item in name:
                    valid_name = False
                    break


            if valid_name and len(name) >= 4: # Implement once module is complete

                # Prone for removal later
                summoner_url = 'https://' + region_dict[region_dict['current']]\
                    .lower() + '.api.riotgames.com/lol/summoner/v4/summoners' \
                               '/by-name/' + name + '?api_key=' + \
                               token_dict['league']

                #print(summoner_url)

                summoner_dict = await summoner_search(name)

                #print(summoner_dict)

                if 'id' not in summoner_dict.keys():
                    await channel.send('The summoner name ' + name + \
                                       ' cannot be found. Names with special '
                                       'characters cannot be searched, '
                                       'otherwise try switching regions.')

                else:
                    await channel.send('Sending info on summoner: ' + name )

                    champ_masteries = summoner_dict['champ_mastery']

                    if len(champ_masteries) < 5:
                        await channel.send('The summoner you searched has less \
                        than five champions played, so only their most played \
                        champions will be displayed')

                    champ = {}  # For exceptions

                    mastery_msg = ''
                    try:
                        for item in champ_masteries:
                            champ = item
                            mastery_msg += champ_id[item['championId']]
                            mastery_msg += ' [lvl ' + str(item['championLevel']) + ']'
                            mastery_msg += ': ' + str(item['championPoints']) + '\n'

                    except KeyError:
                        await channel.send('Missing a champion id reference,'
                                           ' the missing champion\'s id is ' +
                                           champ['championID'])

                    #Ranked info
                    ranked_list = summoner_dict['ranked']
                    if ranked_list == []:
                        ranked_msg = 'Unranked'

                    else:
                        counter = -1
                        for i in range(len(ranked_list)):
                            if ranked_list[i]['queueType'] == 'RANKED_SOLO_5x5':
                                counter = i

                        if counter == -1:
                            ranked_msg = 'Unranked'

                        else:
                            ranked_msg = ranked_list[counter]['tier'] + ' ' + \
                                         ranked_list[counter]['rank']

                    # Time info
                    if summoner_dict['time'] == -1:
                        time_msg = '0'

                    else:
                        time_msg = '~' + str(summoner_dict['time']) + ' minutes'

                        hours_spent = ceil(int(summoner_dict['time'])/60)

                        time_msg += '/~' + str(hours_spent) + ' hours'

                        days_spent = round((int(summoner_dict['time'])/60)/24, 1)

                        time_msg += '/~' + str(days_spent) + ' days'



                    embed = discord.Embed(title='Summoner: ' + name,
                                          description= name + '\'s profile',
                                          color=0x0000ff)
                    '''
                    print('http://avatar.leagueoflegends.com/'
                                            + region_dict['current'].lower() +
                                            '/' + name.replace(' ','+') + '.png')
                                            '''
                    embed.set_thumbnail(url='http://avatar.leagueoflegends.com/'
                                            + region_dict['current'].lower() +
                                            '/' + name.replace(' ','+') + '.png')
                    embed.add_field(name='Level', value= summoner_dict
                    ['summonerLevel'], inline=True)
                    embed.add_field(name='Region', value=region_dict['current'],
                                    inline=True)
                    embed.add_field(name='Rank', value=ranked_msg,
                                    inline=True)
                    embed.add_field(name='Champion Mastery', value=mastery_msg,
                                    inline=True)
                    embed.add_field(name='Time Spent', value=time_msg,
                                    inline=True)
                    embed.add_field(name='More Details',
                                    value='https://na.op.gg/summoner/userName='
                                          + name.replace(' ','+'), inline=True)
                    embed.set_footer(text='LoLInfoTool is not associated with'
                                          ' op.gg or wol.gg')

                    await channel.send(embed=embed)


                # Example: retrieving the icon of me:
                # http://avatar.leagueoflegends.com/na/Ieatyourweapon.png


            else:
                await channel.send('The summoner name ' + name + ' is invalid')





client.run(token_dict['discord'])

