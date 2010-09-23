from twisted.internet import reactor

import sqlite3, string
import minionsLog, minionsRooms, minionsUtils

################################################
# LoadPlayer()
#
# Loads player from database
################################################
def LoadPlayer(player):
    global DB
    try:
        conn     = sqlite3.connect('data\\players.db')
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
        conn     = sqlite3.connect('data\\players.db')
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
        conn     = sqlite3.connect('data\\players.db')
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
        conn     = sqlite3.connect('data\\players.db')
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
        conn     = sqlite3.connect('data\\players.db')
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
        conn     = sqlite3.connect('data\\players.db')
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

################################################
# LoadMessages()
# Loads Messages from database
################################################
def LoadMessages(Sonzo):
    global MessageList
    global DB
    try:
        conn     = sqlite3.connect('data\\messages.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( 'SELECT * from messages')
    except:
        minionsLog.Logit("Failed to get door data from the database.")
    for row in cur:
        minionsUtils.MessageList[row[0]] = str(row[1])
    conn.close()
    print "Loaded %d messages." % (len(minionsUtils.MessageList),)

################################################
# LoadDoors()
#  *** NOT CURRENTLY IN USE ***
# Loads Doors from database
################################################
def LoadDoors(Sonzo):
    global DoorList
    global DB
    try:
        conn     = sqlite3.connect('data\\rooms.db')
        cur      = conn.cursor()
    except:
        minionsLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( 'SELECT * from doors')
    except:
        minionsLog.Logit("Failed to get door data from the database.")
    for row in cur:
        minionsRooms.DoorList[row[0]] = minionsRooms.DoorObj()
        minionsRooms.DoorList[row[0]].DoorNum                         = row[0]
        minionsRooms.DoorList[row[0]].DoorType                        = row[1]
        minionsRooms.DoorList[row[0]].Passable                        = row[2]
        minionsRooms.DoorList[row[0]].DoorStatus                      = row[3]
        minionsRooms.DoorList[row[0]].DoesLock                        = row[4]
        minionsRooms.DoorList[row[0]].Locked                          = row[5]
        minionsRooms.DoorList[row[0]].DoorDesc                        = row[6]
        Room1                                                         = row[7]
        Room2                                                         = row[8]
        minionsRooms.DoorList[row[0]].ExitRoom                        = {Room1: Room2, Room2: Room1}
    conn.close()
    print "Loaded %d doors." % (len(minionsRooms.DoorList),)


#################################################
# LoadRooms1()
#
# Load all rooms from the database
#################################################
def LoadRooms(Sonzo):
    global RoomList
    global DB

    try:
        conn     = sqlite3.connect('data\\rooms.db')
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
        minionsRooms.RoomList[row[0]] = minionsRooms.RoomObj()
        minionsRooms.RoomList[row[0]].RoomNum                         = row[0]
        minionsRooms.RoomList[row[0]].Name                            = str(row[1])
        minionsRooms.RoomList[row[0]].Desc1                           = str(row[2])
        minionsRooms.RoomList[row[0]].Desc2                           = str(row[3])
        minionsRooms.RoomList[row[0]].Desc3                           = str(row[4])
        minionsRooms.RoomList[row[0]].Desc4                           = str(row[5])
        minionsRooms.RoomList[row[0]].Desc5                           = str(row[6])

        # Get door Directions / destinations and fill in Doors dict (hash)
        DoorString                                                    = str(row[7]).split("|")
        for each in DoorString:
            d = each.split(':')

            minionsRooms.RoomList[row[0]].Doors[int(d[0])] = int(d[1])

        minionsRooms.RoomList[row[0]].LightLevel                      = row[8]
        minionsRooms.RoomList[row[0]].RoomSpell                       = row[9]
        minionsRooms.RoomList[row[0]].trap                            = row[10]


    print "Loaded %d rooms." % (len(minionsRooms.RoomList),)

