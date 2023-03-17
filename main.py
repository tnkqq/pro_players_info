import data_based
from pro_player_parser import get_players_list
import time
from pro_player_parser import get_page_info
from data_based import Db_check_exception,None_Gear_exception,None_Specs_exception,Not_found_on_site_exception,None_bio_exception
import prosettings_bot


#update player 
exception_list = []
def add_player(name):
    global exception_list
    try:
        data_based.insert_player_in_db(name) 
    except Db_check_exception as e:
        exception_list.append(f"{name} : already in db...")
        print(f"{name} : already in db...")
    except None_bio_exception as e:
        exception_list.append(f"{name} : haven't bio...")
        print(f"{name} : haven't bio...")
    except None_Gear_exception as e:
        exception_list.append(f"{name} : haven't gear...")
        print(f"{name} : haven't gear...")
    except None_Specs_exception as e:
        print(f"{name} : haven't specs...")
        exception_list.append(f"{name} : haven't specs...")
    except Not_found_on_site_exception as e:
        exception_list.append(f"{name} : not found on prosetting.net")
        

#update data base 
def update_data_base():
    count =1 
    for player in get_players_list():
        print(f"{count} iteration...")
        add_player(player)
        if count%20 ==0:
            print(exception_list)
        count+=1
    

    
#delete player
def delete_player(player):
    data_based.delete_player_from_db(player)



def start_telebot():
    prosettings_bot

    
#clear all 


if __name__ == "__main__":
    pass
    print(f"Exception list : {exception_list}")

# update_data_base()
