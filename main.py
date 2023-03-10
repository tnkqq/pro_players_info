import data_based
from pro_player_parser import get_players_list
import time
from pro_player_parser import get_page_info



#update player 
exception_list = []
def add_player(name):
    global exception_list
    if data_based.insert_player_in_db(name) is not None:
        data_based.insert_player_in_db(name)
    else:
        exception_list.append(name)

        

#update data base 
def update_data_base():
    count =0 
    for player in get_players_list():
        print(f"{player} try to db...")
        add_player(player)
    

    
#delete player
def delete_player(player):
    data_based.delete_player_from_db(player)



#clear all 

#search player 

delete_player("s1mple")
add_player("s1mple")



print(f"Exception list : {exception_list}")
