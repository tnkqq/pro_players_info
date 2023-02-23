
import sqlite3
from pro_player_parser import player_bio_dict,player_gear_dict,player_specs_dict
import uuid
import shortuuid

#id | name | birthday | country | team


def creat_table():
    with sqlite3.connect("db/player_data_base.db") as db:
        
        cursor = db.cursor()

        """creating table"""
        query1 = """CREATE TABLE IF NOT  EXISTS pro_players_table (id INT NOT NULL PRIMARY KEY,Nickname TEXT,Name TEXT,Birthday TEXT,Country TEXT,Team TEXT)"""
        cursor.execute(query1)
bio_insert_info = list(item for item in player_bio_dict.values())
gear_insert_info = list(item for item in player_gear_dict.values())
specs_insert_info = list(item for item in player_specs_dict.values())



def insert_player_in_db(player):
    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor() 
        nickname = bio_insert_info[-1]  
        id = shortuuid.ShortUUID().random(length=4)
        bio_insert_info.append(id)
        print(id)
        check = cursor.execute(f"SELECT nickname from pro_players_table WHERE nickname ='{nickname}'").fetchone()
        
        if check is not None:
            print("Player already in db!")
        else:
            
            cursor.execute("""INSERT INTO pro_players_table (name,Birthday,Country,Team,Nickname,id) VALUES(?,?,?,?,?,?)""",bio_insert_info)
            
        

creat_table()
insert_player_in_db(bio_insert_info)