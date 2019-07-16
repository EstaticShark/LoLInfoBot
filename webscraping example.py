import aiohttp, requests
from bs4 import BeautifulSoup
from config import region_dict

url = 'https://wol.gg/stats/na/Ieatyourweapon/'

soup = requests.get(url)
content_html = BeautifulSoup(soup.content, features='html.parser')

#print(content_html.prettify())

i = content_html.find('div', id = 'time-minutes')
print(i)
print(content_html[i:i+40])