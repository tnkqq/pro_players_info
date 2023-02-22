from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time 
import lxml
import requests


""" func to get ifno from bio table"""
def get_player_bio(src):
    try:
        soup =BeautifulSoup(src,"lxml")
        table=soup.find(class_= "player-bio").find(class_= "intro").find(class_="data").find_all("tr")
        player_table_dict =dict()
        
        for tr in table:
            td = tr.find("td").text.strip()
            th = tr.find("th").text.strip()
            player_table_dict [th] = td 

        return player_table_dict

    except:
        return("Player Bio was NOT FOUND!")

"""func to get player's gear info"""

def get_player_gear(src):
    try:
        soup =BeautifulSoup(src,"lxml")
        gear = soup.find(class_ = "center-container").find (class_ = "equipment").find(id = "gear").find(class_ = "cta-boxes--list").find_all(class_ ="cta-box promo linked ext-link promo linked ext-link")
        gear_table_dict =dict()
        for box_item in gear:
            box_status = box_item.find(class_ = "cta-box_status-tag").text
            gear_name = box_item.find("h4").find("a").text
            
            gear_table_dict [box_status] =gear_name
            
    

        return gear_table_dict
    except:
        return("Player Gear was NOT FOUND!")

""" func to get player pc specs """

def get_player_pc_specs(src):
    soup =BeautifulSoup(src,"lxml")
    specs = soup.find(class_ = "center-container").find (class_ = "equipment").find(id = "pcspecs").find(class_ = "cta-boxes--list").find_all(class_ ="cta-box promo linked ext-link promo linked ext-link")
    
    pc_specs_dict = dict()
    for box_item in specs:
        box_status = box_item.find(class_ = "cta-box_status-tag").text
        specs_name = box_item.find("h4").find("a").text
        pc_specs_dict [box_status] =specs_name
    return pc_specs_dict

    
"""func to get info from page"""

def get_page_info (nickname):

    url = f"https://prosettings.net/players/{nickname}/"
    src = requests.get(url).text

    player_bio_dict = get_player_bio(src)
    player_gear_dict = get_player_gear(src)
    player_specs_dict = get_player_pc_specs(src)
    return player_bio_dict,player_gear_dict,player_specs_dict
    
print(get_page_info("https://prosettings.net/players/s1mple/"))

    
