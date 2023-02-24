
import sqlite3
import pro_player_parser
import uuid
import shortuuid

#id | name | birthday | country | team


def creat_table():
    with sqlite3.connect("db/player_data_base.db") as db:
        
        cursor = db.cursor()

        """creating table"""
        query1 = """CREATE TABLE IF NOT  EXISTS pro_players_table (id INT NOT NULL PRIMARY KEY,Nickname TEXT,Name TEXT,Birthday TEXT,Country TEXT,Team TEXT)"""
        cursor.execute(query1)



def insert_player_in_db(player):
    
    creat_table()
    pro_player_parser.get_page_info(player)
    from pro_player_parser import player_bio_dict,player_gear_dict,player_specs_dict
    
    if player_bio_dict is not None:
        bio_insert_info = list(item for item in player_bio_dict.values())
    else: 
        return (f"{player} havent bio...") 
    
    if player_gear_dict is not None:
        gear_insert_info = list(item for item in player_gear_dict.values())
    else: 
        return  print(f"{player} havent gear...")
    
    if player_specs_dict is  not  None:
        specs_insert_info = list(item for item in player_specs_dict.values())
    else: 
        return print(f"{player} havent specs...")


    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor() 
        nickname = bio_insert_info[-1]  
        id = shortuuid.ShortUUID().random(length=4)
        bio_insert_info.append(id)
        check = cursor.execute(f"SELECT nickname from pro_players_table WHERE nickname ='{nickname}'").fetchone()
        if check is not None:

            print("Player already in db!")

        else:
            
            cursor.execute("""INSERT INTO pro_players_table (name,Birthday,Country,Team,Nickname,id) VALUES(?,?,?,?,?,?)""",bio_insert_info)
            print(f"{player} was added in db..." )
    



def delete_player_from_db(player):
    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor()
        try:
            cursor.execute(f"DELETE  FROM pro_players_table WHERE nickname = '{player}'")
            return print(f"{player} was deleted from db...")
        except:
            return print(f"{player} already not in db...")
            

    
        
