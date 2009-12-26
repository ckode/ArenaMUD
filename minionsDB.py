import sqlite3, minionsLog

################################################
# LoadPlayer()
#
# Loads player from database
################################################
def LoadPlayer(player, name):
    global DB
    try:
       conn = sqlite.connect(DB)
    except:
       minionsLog.Logit("Failed to open database!")
       
       
def GetUserID(name):
    return 0
    
def CreatePlayer(player):
    global DB
    data = [player.name, player.lastname, player.password, player.hp, player.mana, player.mr, player.stealth]

    try:
        conn     = sqlite.connect('minions.db')
        cursor   = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()
    # Insert new player into the database
    try:
        cursor.execute( 'INSERT INTO player (name, lastname, password, hp, mana, mr, stealth) values ("?", "?", "?", ?, ?, ?, ?)', data )
        conn.commit()
    except:
        minionsLog.Logit("Failed to insert new player into player table!")
    # Get and return players ID number (primary key)
    try:
        cursor.execute( 'SELECT id from player where name = ?', player.name)
    except:
        minionsLog.Logit("Failed to get users ID after creating user in database.")
    return cursor.fetchone()[0]
