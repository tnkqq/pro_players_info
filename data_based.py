
import sqlite3
import pro_player_parser
import uuid
import shortuuid

#id | name | birthday | country | team


class Db_check_exception(Exception):
    pass
class None_bio_exception(Exception):
    pass
class None_Gear_exception(Exception):
    pass
class None_Specs_exception(Exception):
    pass
class Not_found_on_site_exception(Exception):
    pass


def creat_table():
    """Bio,Gear,Specs tables"""
    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor()
        
        query1 = """CREATE TABLE IF NOT  EXISTS pro_players_table (id INT NOT NULL PRIMARY KEY,Nickname TEXT,Name TEXT,Birthday TEXT,Country TEXT,Team TEXT)"""
        query2 = """CREATE TABLE IF NOT  EXISTS pro_players_gear_table (player_id CHAR NOT NULL PRIMARY KEY,FOREIGN KEY(player_id) REFERENCES pro_players_table(id) )"""     
        query3 = """CREATE TABLE IF NOT  EXISTS pro_players_specs_table (player_id CHAR NOT NULL PRIMARY KEY,FOREIGN KEY(player_id) REFERENCES pro_players_table(id) )"""     
        
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
    
    


def insert_player_in_db(player):
    creat_table()
    try:
        pro_player_parser.get_page_info(player)
    except:
        raise Not_found_on_site_exception
    else:
        from pro_player_parser import player_bio_dict,player_gear_dict,player_specs_dict
            
        
        bio_insert_info = list(item for item in player_bio_dict.values())
        nickname = player
        if len(bio_insert_info)<5:
            raise None_bio_exception
        with sqlite3.connect("db/player_data_base.db",isolation_level=None) as db:
            cursor = db.cursor() 
            id = shortuuid.ShortUUID().random(length=4)
            bio_insert_info.append(id)
            check = cursor.execute(f"""SELECT nickname FROM pro_players_table WHERE nickname ='{nickname}'""").fetchone()
            if check is not None:
                raise Db_check_exception
            else:
                cursor.execute("""INSERT INTO pro_players_table (name,Birthday,Country,Team,Nickname,id) VALUES(?,?,?,?,?,?)""",bio_insert_info)
                #print(f"{player} was added in db..." )
                cursor.close()
            if player_gear_dict is None:
                raise None_Gear_exception
            else: player_gear_table(id,player_gear_dict)

            if player_specs_dict is None:
                raise None_Specs_exception
            else: player_specs_table(id,player_specs_dict)

                
        
        #specs_gear_table(player)
    
    
        
#print(insert_player_in_db("pio"))

def delete_player_from_db(player):
    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor()
        try:
            cursor.execute(f"DELETE  FROM pro_players_table WHERE nickname = '{player}'")
            return print(f"{player} was deleted from db...")
        except:
            return print(f"{player} already not in db...")
        

  
def player_gear_table(id,gear_dict):
    
    id= str(id)
    
    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor()
        
        try:    
            cursor.execute("""INSERT INTO pro_players_gear_table(player_id) VALUES(?) """,(id,))
        except: pass

        for key,value in gear_dict.items():
            try:
                cursor.execute("""ALTER TABLE pro_players_gear_table ADD COLUMN {} TEXT""".format(key))
            except: pass
            cursor.execute("""UPDATE pro_players_gear_table SET {} = ? WHERE player_id = ? """.format(key),(value,id))
    cursor.close()


def player_specs_table(id,specs_dict):
    id = id 
    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor()

        try:
            cursor.execute("""INSERT INTO pro_players_specs_table(player_id) VALUES(?) """,(id,))
        except: pass

        for key,value in specs_dict.items():
            try:
                cursor.execute("""ALTER TABLE pro_players_specs_table ADD COLUMN "{}" TEXT""".format(key))
            except: pass
            cursor.execute("""UPDATE pro_players_specs_table SET "{}" = ? WHERE player_id = ? """.format(key),(value,id))

  
def player_info(player):
    bio=dict()
    gear=dict()
    #specs=dict()
    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor()
        bio_data=cursor.execute("""SELECT * FROM pro_players_table WHERE Nickname = "{}" """.format(player))
        columns = [desc[0] for desc in bio_data.description]
        for row in bio_data.fetchall():
            bio = dict(zip(columns,row))
        player_id = bio["id"]
        gear_data = cursor.execute("""SELECT * FROM pro_players_gear_table WHERE player_id = "{}" """.format(player_id))
        columns = [desc[0] for desc in gear_data.description]
        for row in gear_data.fetchall():
            gear = dict(zip(columns,row))
        specs_data = cursor.execute("""SELECT * FROM pro_players_specs_table WHERE player_id = "{}" """.format(player_id))
        columns = [desc[0] for desc in specs_data.description]
        for row in specs_data.fetchall():
            specs = dict(zip(columns,row))
        
    
    return bio,gear,specs
            


def get_team_list(team):
    with sqlite3.connect("db/player_data_base.db") as db:
        cursor = db.cursor()
        players_list = cursor.execute("""SELECT Nickname FROM pro_players_table WHERE Team = "{}" """.format(team)).fetchall()
    players_list = [x[0] for x in players_list]
    print(f"player list at db {players_list}")
    return players_list


