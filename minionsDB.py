from twisted.internet import reactor

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

    # Defined here for earier to read code below
    NONE         =  0
    NORTH        =  1
    NORTHEAST    =  2
    EAST         =  3
    SOUTHEAST    =  4
    SOUTH        =  5
    SOUTHWEST    =  6
    WEST         =  7
    NORTHWEST    =  8
    UP           =  9
    DOWN         = 10

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
        # Room
        minionsRooms.RoomList[row[0]] = minionsRooms.Room()
        minionsRooms.RoomList[row[0]].RoomNum                         = row[0]
        minionsRooms.RoomList[row[0]].Name                            = str(row[1])
        minionsRooms.RoomList[row[0]].Description                     = str(row[2])
        minionsRooms.RoomList[row[0]].RoomType                        = row[3]
        minionsRooms.RoomList[row[0]].LightLevel                      = row[4]
        minionsRooms.RoomList[row[0]].SecretPhrase                    = str(row[5])
        minionsRooms.RoomList[row[0]].PhaseFunctionID                 = row[6]
        minionsRooms.RoomList[row[0]].ActionID                        = row[7]

        # Door specific attributes
        minionsRooms.RoomList[row[0]].Doors[NORTH].DoorType           = row[8]
        minionsRooms.RoomList[row[0]].Doors[NORTH].ToRoom             = row[9]
        minionsRooms.RoomList[row[0]].Doors[NORTH].DoorStatus         = row[10]
        minionsRooms.RoomList[row[0]].Doors[NORTH].DoesLock           = row[11]
        minionsRooms.RoomList[row[0]].Doors[NORTH].RequiredKey        = row[12]
        minionsRooms.RoomList[row[0]].Doors[NORTH].PickDiff           = row[13]
        minionsRooms.RoomList[row[0]].Doors[NORTH].Passable           = row[14]
        minionsRooms.RoomList[row[0]].Doors[NORTH].Exits[1]           = str(row[15])
        minionsRooms.RoomList[row[0]].Doors[NORTH].Exits[2]           = str(row[16])
        if minionsRooms.RoomList[row[0]].Doors[NORTH].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].DoorType       = row[17]
        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].ToRoom         = row[18]
        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].DoorStatus     = row[19]
        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].DoesLock       = row[20]
        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].RequiredKey    = row[21]
        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].PickDiff       = row[22]
        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].Passable       = row[23]
        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].Exits[1]       = str(row[24])
        minionsRooms.RoomList[row[0]].Doors[NORTHEAST].Exits[2]       = str(row[25])
        if minionsRooms.RoomList[row[0]].Doors[NORTHEAST].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[EAST].DoorType            = row[26]
        minionsRooms.RoomList[row[0]].Doors[EAST].ToRoom              = row[27]
        minionsRooms.RoomList[row[0]].Doors[EAST].DoorStatus          = row[28]
        minionsRooms.RoomList[row[0]].Doors[EAST].DoesLock            = row[29]
        minionsRooms.RoomList[row[0]].Doors[EAST].RequiredKey         = row[30]
        minionsRooms.RoomList[row[0]].Doors[EAST].PickDiff            = row[31]
        minionsRooms.RoomList[row[0]].Doors[EAST].Passable            = row[32]
        minionsRooms.RoomList[row[0]].Doors[EAST].Exits[1]            = str(row[33])
        minionsRooms.RoomList[row[0]].Doors[EAST].Exits[2]            = str(row[34])
        if minionsRooms.RoomList[row[0]].Doors[EAST].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].DoorType       = row[35]
        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].ToRoom         = row[36]
        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].DoorStatus     = row[37]
        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].DoesLock       = row[38]
        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].RequiredKey    = row[39]
        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].PickDiff       = row[40]
        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].Passable       = row[41]
        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].Exits[1]       = str(row[42])
        minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].Exits[2]       = str(row[43])
        if minionsRooms.RoomList[row[0]].Doors[SOUTHEAST].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[SOUTH].DoorType           = row[44]
        minionsRooms.RoomList[row[0]].Doors[SOUTH].ToRoom             = row[45]
        minionsRooms.RoomList[row[0]].Doors[SOUTH].DoorStatus         = row[46]
        minionsRooms.RoomList[row[0]].Doors[SOUTH].DoesLock           = row[47]
        minionsRooms.RoomList[row[0]].Doors[SOUTH].RequiredKey        = row[48]
        minionsRooms.RoomList[row[0]].Doors[SOUTH].PickDiff           = row[49]
        minionsRooms.RoomList[row[0]].Doors[SOUTH].Passable           = row[50]
        minionsRooms.RoomList[row[0]].Doors[SOUTH].Exits[1]           = str(row[51])
        minionsRooms.RoomList[row[0]].Doors[SOUTH].Exits[2]           = str(row[52])
        if minionsRooms.RoomList[row[0]].Doors[SOUTH].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].DoorType       = row[53]
        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].ToRoom         = row[54]
        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].DoorStatus     = row[55]
        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].DoesLock       = row[56]
        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].RequiredKey    = row[57]
        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].PickDiff       = row[58]
        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].Passable       = row[59]
        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].Exits[1]       = str(row[60])
        minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].Exits[2]       = str(row[61])
        if minionsRooms.RoomList[row[0]].Doors[SOUTHWEST].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[WEST].DoorType           = row[62]
        minionsRooms.RoomList[row[0]].Doors[WEST].ToRoom             = row[63]
        minionsRooms.RoomList[row[0]].Doors[WEST].DoorStatus         = row[64]
        minionsRooms.RoomList[row[0]].Doors[WEST].DoesLock           = row[65]
        minionsRooms.RoomList[row[0]].Doors[WEST].RequiredKey        = row[66]
        minionsRooms.RoomList[row[0]].Doors[WEST].PickDiff           = row[67]
        minionsRooms.RoomList[row[0]].Doors[WEST].Passable           = row[68]
        minionsRooms.RoomList[row[0]].Doors[WEST].Exits[1]           = str(row[69])
        minionsRooms.RoomList[row[0]].Doors[WEST].Exits[2]           = str(row[70])
        if minionsRooms.RoomList[row[0]].Doors[WEST].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].DoorType       = row[71]
        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].ToRoom         = row[72]
        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].DoorStatus     = row[73]
        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].DoesLock       = row[74]
        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].RequiredKey    = row[75]
        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].PickDiff       = row[76]
        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].Passable       = row[77]
        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].Exits[1]       = str(row[78])
        minionsRooms.RoomList[row[0]].Doors[NORTHWEST].Exits[2]       = str(row[79])
        if minionsRooms.RoomList[row[0]].Doors[NORTHWEST].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[UP].DoorType              = row[80]
        minionsRooms.RoomList[row[0]].Doors[UP].ToRoom                = row[81]
        minionsRooms.RoomList[row[0]].Doors[UP].DoorStatus            = row[82]
        minionsRooms.RoomList[row[0]].Doors[UP].DoesLock              = row[83]
        minionsRooms.RoomList[row[0]].Doors[UP].RequiredKey           = row[84]
        minionsRooms.RoomList[row[0]].Doors[UP].PickDiff              = row[85]
        minionsRooms.RoomList[row[0]].Doors[UP].Passable              = row[86]
        minionsRooms.RoomList[row[0]].Doors[UP].Exits[1]              = str(row[87])
        minionsRooms.RoomList[row[0]].Doors[UP].Exits[2]              = str(row[88])
        if minionsRooms.RoomList[row[0]].Doors[UP].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

        minionsRooms.RoomList[row[0]].Doors[DOWN].DoorType           = row[89]
        minionsRooms.RoomList[row[0]].Doors[DOWN].ToRoom             = row[90]
        minionsRooms.RoomList[row[0]].Doors[DOWN].DoorStatus         = row[91]
        minionsRooms.RoomList[row[0]].Doors[DOWN].DoesLock           = row[92]
        minionsRooms.RoomList[row[0]].Doors[DOWN].RequiredKey        = row[93]
        minionsRooms.RoomList[row[0]].Doors[DOWN].PickDiff           = row[94]
        minionsRooms.RoomList[row[0]].Doors[DOWN].Passable           = row[95]
        minionsRooms.RoomList[row[0]].Doors[DOWN].Exits[1]           = str(row[96])
        minionsRooms.RoomList[row[0]].Doors[DOWN].Exits[2]           = str(row[97])
        if minionsRooms.RoomList[row[0]].Doors[DOWN].DoesLock == 1:
           minionsRooms.RoomList[row[0]].DoorLocked = 1

    print "Loaded %d rooms." % (len(minionsRooms.RoomList),)
