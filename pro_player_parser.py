from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time 
import lxml
import requests

def get_page (nickname):

    url = f"https://prosettings.net/players/{nickname}/"
    src = requests.get(url).text

    try:
        soup =BeautifulSoup(src,"lxml")
        table=soup.find(class_= "player-bio").find(class_= "intro").find(class_="data").find_all("tr")
        player_table_dict =dict()
        for tr in table:
            td = tr.find("td").text.strip()
            th = tr.find("th").text.strip()
            player_table_dict [th] =td 

        return player_table_dict
    except:
        return("smthng wrong")
    


print(get_page("s1mple"))