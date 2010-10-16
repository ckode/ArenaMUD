#  ArenaMUD - A multiplayer combat game - http://arenamud.david-c-brown.com
#  Copyright (C) 2009, 2010 - David C Brown & Mark Richardson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from twisted.internet import reactor

import sqlite3, string
import amLog, amRooms, amUtils, amRace

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
        amLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( 'SELECT * from players where name = ?', (player.name,))
    except:
        amLog.Logit("Failed to get player data from the database.")
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
        amLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( "SELECT id from players where name=?", (name,) )
    except:
        amLog.Logit("Failed to get users ID from the database.")

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
        amLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( "SELECT passwd from players where name=?", (name,))
    except:
        amLog.Logit("Failed to get users password from the database.")
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
        amLog.Logit("Failed to open database!")
        player.Shutdown()
    # Insert new player into the database
    try:
        cur.execute( 'INSERT INTO players (name, lastname, passwd, hp, maxhp, mana, maxmana, mr, stealth, room) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data )
        conn.commit()
    except:
        amLog.Logit("Failed to insert new player into player table!")
    # Get and return players ID number (primary key)
    try:
        cur.execute( 'SELECT id from players where name = ?', (player.name,))
    except:
        amLog.Logit("Failed to get users ID after creating user in database.")
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
        amLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( "UPDATE players SET passwd=? WHERE name =?", (password, name))
        conn.commit()
    except:
        amLog.Logit("Failed to update users password from the database where user was: %s" % (name,))
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
        amLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( "UPDATE players SET lastname=? WHERE name =?", (lastname, name))
        conn.commit()
    except:
        amLog.Logit("Failed to update users lastname from the database where user was: %s" % (name,))
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
        amLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( 'SELECT * from messages')
    except:
        amLog.Logit("Failed to get door data from the database.")
    for row in cur:
        amUtils.MessageList[row[0]] = str(row[1])
    conn.close()
    print "Loaded %d messages." % (len(amUtils.MessageList),)

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
        amLog.Logit("Failed to open database!")
        player.Shutdown()

    try:
        cur.execute( 'SELECT * from doors')
    except:
        amLog.Logit("Failed to get door data from the database.")
    for row in cur:
        amRooms.DoorList[row[0]] = amRooms.DoorObj()
        amRooms.DoorList[row[0]].DoorNum                         = row[0]
        amRooms.DoorList[row[0]].DoorType                        = row[1]
        amRooms.DoorList[row[0]].Passable                        = row[2]
        amRooms.DoorList[row[0]].DoorStatus                      = row[3]
        amRooms.DoorList[row[0]].DoesLock                        = row[4]
        amRooms.DoorList[row[0]].Locked                          = row[5]
        amRooms.DoorList[row[0]].DoorDesc                        = row[6]
        Room1                                                         = row[7]
        Room2                                                         = row[8]
        amRooms.DoorList[row[0]].ExitRoom                        = {Room1: Room2, Room2: Room1}
    conn.close()
    print "Loaded %d doors." % (len(amRooms.DoorList),)


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
        amLog.Logit("Failed to open database!")
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM rooms")
    except:
        amLog.Logit("Failed to query database for room information!")
    for row in cur:
        # Room
        amRooms.RoomList[row[0]] = amRooms.RoomObj()
        amRooms.RoomList[row[0]].RoomNum                         = row[0]
        amRooms.RoomList[row[0]].Name                            = str(row[1])
        amRooms.RoomList[row[0]].Desc1                           = str(row[2])
        amRooms.RoomList[row[0]].Desc2                           = str(row[3])
        amRooms.RoomList[row[0]].Desc3                           = str(row[4])
        amRooms.RoomList[row[0]].Desc4                           = str(row[5])
        amRooms.RoomList[row[0]].Desc5                           = str(row[6])

        # Get door Directions / destinations and fill in Doors dict (hash)
        DoorString                                                    = str(row[7]).split("|")
        for each in DoorString:
            d = each.split(':')

            amRooms.RoomList[row[0]].Doors[int(d[0])] = int(d[1])

        amRooms.RoomList[row[0]].LightLevel                      = row[8]
        amRooms.RoomList[row[0]].RoomSpell                       = row[9]
        amRooms.RoomList[row[0]].RoomTrap                        = row[10]
        amRooms.RoomList[row[0]].NoSpawn                         = row[11]


    print "Loaded %d rooms." % (len(amRooms.RoomList),)

#################################################
# LoadRoomSpells()
#
# Load all rooms spells from the database
#################################################
def LoadRoomSpells(Sonzo):
    global RoomSpellList
    global DB

    try:
        conn     = sqlite3.connect('data\\rooms.db')
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database!")
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM RoomSpells")
    except:
        amLog.Logit("Failed to query database for room information!")
    for row in cur:
        # Room
        amRooms.RoomSpellList[row[0]] = amRooms.RoomSpell()
        amRooms.RoomSpellList[row[0]].RoomNum                         = row[0]
        amRooms.RoomSpellList[row[0]].hp_adjust                       = row[1]
        amRooms.RoomSpellList[row[0]].desc                            = str(row[2])

    print "Loaded %d room spells." % (len(amRooms.RoomSpellList),)

#################################################
# LoadRoomTraps()
#
# Load all room traps from the database
#################################################
def LoadRoomTraps(Sonzo):
    global RoomTrapsList
    global DB

    try:
        conn     = sqlite3.connect('data\\rooms.db')
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database!")
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM RoomTraps")
    except:
        amLog.Logit("Failed to query database for room information!")
    for row in cur:
        # Room
        amRooms.RoomTrapList[row[0]] = amRooms.RoomSpell()
        amRooms.RoomTrapList[row[0]].RoomNum                         = row[0]
        amRooms.RoomTrapList[row[0]].stat                            = row[1]
        amRooms.RoomTrapList[row[0]].value                           = row[2]
        amRooms.RoomTrapList[row[0]].duration                        = row[3]
        amRooms.RoomTrapList[row[0]].playerdesc                      = str(row[4])
        amRooms.RoomTrapList[row[0]].roomdesc                        = str(row[5])

    print "Loaded %d room traps." % (len(amRooms.RoomTrapList),)

###########################################
# Load Classes
###########################################
def LoadClasses(Sonzo):
    global ClassList
    global DB

    try:
        conn     = sqlite3.connect('data\\rcdata.db')
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database!")
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM class")
    except:
        amLog.Logit("Failed to query database for room information!")
    for row in cur:
        # Room
        amRace.ClassList[row[0]] = amRace.Class()
        amRace.ClassList[row[0]].id                              = row[0]
        amRace.ClassList[row[0]].name                            = str(row[1])
        amRace.ClassList[row[0]].desc                            = str(row[2])
        amRace.ClassList[row[0]].hpbonus                         = row[3]
        amRace.ClassList[row[0]].mindamage                       = row[4]
        amRace.ClassList[row[0]].maxdamage                       = row[5]
        amRace.ClassList[row[0]].BaseArmor                       = row[6]
        amRace.ClassList[row[0]].MageryType                      = row[7]
        amRace.ClassList[row[0]].stealth                         = row[8]
        amRace.ClassList[row[0]].weapontext                      = row[9]

    print "Loaded %d classes." % (len(amRace.ClassList),)


########################################
# Load Races
########################################
def LoadRaces(Sonzo):
    global ClassList
    global DB

    try:
        conn     = sqlite3.connect('data\\rcdata.db')
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database!")
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM race")
    except:
        amLog.Logit("Failed to query database for room information!")
    for row in cur:
        # Room
        amRace.RaceList[row[0]] = amRace.Race()
        amRace.RaceList[row[0]].id                              = row[0]
        amRace.RaceList[row[0]].name                            = str(row[1])
        amRace.RaceList[row[0]].desc                            = str(row[2])
        amRace.RaceList[row[0]].basehp                          = row[3]
        amRace.RaceList[row[0]].damagebonus                     = row[4]
        amRace.RaceList[row[0]].castingbonus                    = row[5]
        amRace.RaceList[row[0]].vision                          = row[6]
        amRace.RaceList[row[0]].defensebonus                    = row[7]
        amRace.RaceList[row[0]].attackbonus                     = row[8]
        amRace.RaceList[row[0]].stealth                         = row[9]

    print "Loaded %d races." % (len(amRace.RaceList),)


######################################################
#    LoadAnsiScreens()
#    Load up any ansi screens here
######################################################
def LoadAnsiScreens():
    global AnsiScreen
    f = open('data\\splash.ans','rb')
    amRooms.AnsiScreen = f.read()
    f.close()
