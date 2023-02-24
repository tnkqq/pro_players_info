import data_based
from pro_player_parser import get_players_list
import time
from pro_player_parser import get_page_info

#update player 
def add_player(name):
    global exception_list
    try:
        data_based.insert_player_in_db(name)
    except:
        exception_list = []
        exception_list.append(name)
        



#update data base 
def update_data_base():
    count =0 
    for player in get_players_list():
        print(f"{player} try to db...")
        data_based.insert_player_in_db(player)
    print()    

    


#delete player 

def delete_player(player):
    data_based.delete_player_from_db(player)

data_based.insert_player_in_db("GeT_RiGhT")


#clear all 

#search player 

