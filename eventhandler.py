import discord
import aiohttp
from config import token_dict, region_dict

client = discord.Client()


@client.event  # Event for when bot is ready
async def on_ready():
    print("LoL Info Tool is ready!")

@client.event
async def on_message(msg):
    if len(msg.content) > 0:


        # Welcome Message: Work in progress
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
            valid_name = True
            punc =',./;\'[]<>?:\"{}!@#$%^&*()_+-='
            for item in punc:
                if item in msg.content[10:]:
                    valid_name = False
                    break

            if valid_name: # Implement once module is complete
                pass


client.run(token_dict['discord'])

