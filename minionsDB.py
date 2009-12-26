import sqlite3, minionsLog

################################################
# LoadPlayer()
#
# Loads player from database
################################################
def LoadPlayer(player, name):
    global DB
    try:
        conn     = sqlite3.connect('minions.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( 'SELECT * from players where name = ?', (player.name,))
    except:
        minionsLog.Logit("Failed to get player data from the database.")
    row = cur.fetchone()
    player.lastname = row[2]
    player.password = row[3]
    player.hp       = row[4]
    player.mana     = row[5]
    player.mr       = row[6]
    player.stealth  = row[7]
    conn.close()

       
#################################################
# GetUserID()
#
# Returns players userid number by their username.
#################################################
def GetUserID(name):
    global DB
    
    try:
        conn     = sqlite3.connect('minions.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( "SELECT id from players where name=?", (name,))
    except:
        minionsLog.Logit("Failed to get users ID from the database.")

    conn.close()
    return cur.rowcount



#################################################
# GetPassword()
#
# Returns players password number by their username.
#################################################
def GetPassword(name):
    global DB
    
    try:
        conn     = sqlite3.connect('minions.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( "SELECT passwd from players where name=?", (name,))
    except:
        minionsLog.Logit("Failed to get users password from the database.")
    pw = cur.fetchone()[0]
    conn.close()
    return pw

########################################################
# CreatePlayer()
#
# Creates a new player in the database
########################################################
def CreatePlayer(player):
    global DB
    #return 0
    data = [player.name, player.lastname, player.password, player.hp, player.mana, player.mr, player.stealth]

    try:
        conn     = sqlite3.connect('minions.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()
    # Insert new player into the database
    try:
        cur.execute( 'INSERT INTO players (name, lastname, passwd, hp, mana, mr, stealth) values (?, ?, ?, ?, ?, ?, ?)', data )
        conn.commit()
    except:
        minionsLog.Logit("Failed to insert new player into player table!")
    # Get and return players ID number (primary key)
    try:
        cur.execute( 'SELECT id from players where name = ?', (player.name,))
    except:
        minionsLog.Logit("Failed to get users ID after creating user in database.")
    uid = cur.fetchone()[0]
    conn.close()
    return uid