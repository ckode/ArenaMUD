import sqlite3, string
import minionsLog, minionsRooms

################################################
# LoadPlayer()
#
# Loads player from database
################################################
def LoadPlayer(player):
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
    #if row[2] == None:
    #   player.lastname = " "
    #else:
    #   player.lastname = row[2]
    player.lastname = str(row[2])
    player.password = str(row[3])
    player.hp       = row[4]
    player.mana     = row[5]
    player.mr       = row[6]
    player.stealth  = row[7]
    player.room     = row[8]
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
        cur.execute( "SELECT id from players where name=?", (name,) )
    except:
        minionsLog.Logit("Failed to get users ID from the database.")

    try:
        uid = cur.fetchone()[0]
    except:
        return 0
    conn.close()
    return uid



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
    data = [player.name, player.lastname, player.password, player.hp, player.maxhp, player.mana, player.maxmana, player.mr, player.stealth, player.room]

    try:
        conn     = sqlite3.connect('minions.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()
    # Insert new player into the database
    try:
        cur.execute( 'INSERT INTO players (name, lastname, passwd, hp, maxhp, mana, maxmana, mr, stealth, room) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data )
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
    
#################################################
# ChangePassword()
#
# Changes players password
#################################################
def ChangePassword(name, password):
    global DB

    try:
        conn     = sqlite3.connect('minions.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( "UPDATE players SET passwd=? WHERE name =?", (password, name))
        conn.commit()
    except:
        minionsLog.Logit("Failed to update users password from the database where user was: %s" % (name,))
    conn.close()

#################################################
# ChangeLastname()
#
# Changes players Lastname
#################################################
def ChangeLastname(name, lastname):
    global DB

    try:
        conn     = sqlite3.connect('minions.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( "UPDATE players SET lastname=? WHERE name =?", (lastname, name))
        conn.commit()
    except:
        minionsLog.Logit("Failed to update users lastname from the database where user was: %s" % (name,))
    conn.close()

#################################################
# LoadRooms()
#
# Load all rooms from the database
#################################################
def LoadRooms(Sonzo):
    global RoomList
    global DB

    try:
        conn     = sqlite3.connect('minions.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM rooms")
    except:
        minionsLog.Logit("Failed to query database for room information!")
    for row in cur:
        minionsRooms.RoomList[row[0]] = minionsRooms.Room()
        minionsRooms.RoomList[row[0]].RoomNum            = row[0]
        minionsRooms.RoomList[row[0]].Name               = str(row[1])
        minionsRooms.RoomList[row[0]].Description        = str(row[2])
        minionsRooms.RoomList[row[0]].N                  = row[3]
        minionsRooms.RoomList[row[0]].NE                 = row[4]
        minionsRooms.RoomList[row[0]].E                  = row[5]
        minionsRooms.RoomList[row[0]].SE                 = row[6]
        minionsRooms.RoomList[row[0]].S                  = row[7]
        minionsRooms.RoomList[row[0]].SW                 = row[8]
        minionsRooms.RoomList[row[0]].W                  = row[9]
        minionsRooms.RoomList[row[0]].NW                 = row[10]
        minionsRooms.RoomList[row[0]].U                  = row[11]
        minionsRooms.RoomList[row[0]].D                  = row[12]
        minionsRooms.RoomList[row[0]].exits              = str(row[13])

    print "Loaded %d rooms." % (len(minionsRooms.RoomList),)
