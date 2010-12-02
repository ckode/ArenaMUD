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
import amSpells

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


#===============================================
# LoadSpellsAndItems()
# Loads all class spells and items
#===============================================
def LoadSpellsAndItems( Sonzo ):
    # Sub function to check for errors while assigning the spell effects
    def AssignSpell( curSpellListItem, effect ):
        try: 
            sp = effect.split(":")
        except:
            amLog.Logit("Error loading spell effect, could split effect by a colon. Effect: %s" % ( effect ) )
            return
        
        try:
            curSpellListItem.effects[ int(sp[0])] = sp[1]
        except:
            amLog.Logit("Error loading spell effect, Spell ID isn't an integer.  Effect: %s" % ( sp[0] ) )
            return
              
    
    # Main body of LoadSpellAndItems() function
    Spells   = {}
    Items    = {}

    try:
        conn     = sqlite3.connect( 'data\\rcdata.db' )
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database: rcdata.db" )
        player.Shutdown()

    try:
        cur.execute( 'SELECT * from spells_items')
    except:
        amLog.Logit("Failed to get door data from the database.")
    for row in cur:
        SpellIndex = str(row[2])
        Spells[SpellIndex]                                 = amSpells.Spells()
        Spells[SpellIndex].SpellID                         = row[0]
        Spells[SpellIndex].name                            = str(row[1])
        Spells[SpellIndex].cmd                             = str(row[2])
        Spells[SpellIndex].stype                           = row[3]
        Spells[SpellIndex].CoolDown                        = row[4]
        Spells[SpellIndex].UsedOn                          = row[5]
        Spells[SpellIndex].Class                           = row[6]
        Spells[SpellIndex].duration                        = row[7]
        Spells[SpellIndex].durationEffect                  = row[8]
        effectString                                       = str(row[9]).split("|")
        for each in effectString:
            # Check for errors when assigning with subfunction
            AssignSpell( Spells[SpellIndex], each )
        
        Spells[SpellIndex].gesture                         = str(row[10])
        Spells[SpellIndex].effectText                      = str(row[11])
        Spells[SpellIndex].spellTextSelf                   = str(row[12])
        Spells[SpellIndex].spellTextRoom                   = str(row[13])
        Spells[SpellIndex].spellTextVictim                 = str(row[14])
        Spells[SpellIndex].WearOffText                     = str(row[15])
        Spells[SpellIndex].statusText                      = str(row[16])
        
        # If it's actually an item, assign it to Items and delete from Spells.
        if Spells[SpellIndex].stype == 0:
            Items[row[0]] = Spells[SpellIndex]
            del Spells[SpellIndex]
    
        
    conn.close()
    print "Spells loaded: %s Spawn Items loaded: %i" % ( len(Spells), len(Items) )
    return Spells, Items
################################################
# LoadDoors()
# Loads Doors from database
################################################
def LoadDoors( MapDB ):
    Doors = {}

    try:
        conn     = sqlite3.connect( MapDB )
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database: %s" % ( MapDB ) )
        player.Shutdown()

    try:
        cur.execute( 'SELECT * from doors')
    except:
        amLog.Logit("Failed to get door data from the database.")
    for row in cur:
        Doors[row[0]]                                 = amRooms.DoorObj()
        Doors[row[0]].DoorNum                         = row[0]
        Doors[row[0]].DoorType                        = row[1]
        Doors[row[0]].Passable                        = row[2]
        Doors[row[0]].DoorStatus                      = row[3]
        Doors[row[0]].DoesLock                        = row[4]
        Doors[row[0]].Locked                          = row[5]
        Doors[row[0]].DoorDesc                        = row[6]
        Room1                                         = row[7]
        Room2                                         = row[8]
        Doors[row[0]].ExitRoom                        = {Room1: Room2, Room2: Room1}

    conn.close()
    return Doors


#################################################
# LoadRooms()
# Load all rooms from the database
#################################################
def LoadRooms( MapDB ):
    Rooms = {}

    try:
        conn     = sqlite3.connect( MapDB )
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database: %s" % ( MapDB ) )
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM rooms")
    except:
        amLog.Logit("Failed to query database for room information!")
    for row in cur:
        # Room
        Rooms[row[0]]                                 = amRooms.RoomObj()
        Rooms[row[0]].RoomNum                         = row[0]
        Rooms[row[0]].Name                            = str(row[1])
        Rooms[row[0]].Desc1                           = str(row[2])
        Rooms[row[0]].Desc2                           = str(row[3])
        Rooms[row[0]].Desc3                           = str(row[4])
        Rooms[row[0]].Desc4                           = str(row[5])
        Rooms[row[0]].Desc5                           = str(row[6])

        # Get door Directions / destinations and fill in Doors dict (hash)
        DoorString                                    = str(row[7]).split("|")
        for each in DoorString:
            d = each.split(':')

            Rooms[row[0]].Doors[int(d[0])] = int(d[1])

        Rooms[row[0]].LightLevel                      = row[8]
        Rooms[row[0]].RoomSpell                       = row[9]
        Rooms[row[0]].RoomTrap                        = row[10]
        Rooms[row[0]].NoSpawn                         = row[11]


    return Rooms


#################################################
# LoadRoomSpells()
# Load all rooms spells from the database
#################################################
def LoadRoomSpells( MapDB ):
    RoomSpells = {}

    try:
        conn     = sqlite3.connect( MapDB )
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database: %s" % ( MapDB ) )
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM RoomSpells")
    except:
        amLog.Logit("Failed to query database for room information!")
    for row in cur:
        # Room
        RoomSpells[row[0]]                                 = amRooms.RoomSpell()
        RoomSpells[row[0]].RoomNum                         = row[0]
        RoomSpells[row[0]].hp_adjust                       = row[1]
        RoomSpells[row[0]].desc                            = str(row[2])

    return RoomSpells




#################################################
# LoadRoomTraps()
# Load all room traps from the database
#################################################
def LoadRoomTraps( MapDB ):
    RoomTraps = {}

    try:
        conn     = sqlite3.connect( MapDB )
        cur      = conn.cursor()
    except:
        amLog.Logit("Failed to open database: %s" % ( MapDB ) )
        player.Shutdown()
    try:
        cur.execute( "SELECT * FROM RoomTraps")
    except:
        amLog.Logit("Failed to query database for room information!")
    for row in cur:
        # Room
        RoomTraps[row[0]] = amRooms.RoomSpell()
        RoomTraps[row[0]].RoomNum                         = row[0]
        RoomTraps[row[0]].stat                            = row[1]
        RoomTraps[row[0]].value                           = row[2]
        RoomTraps[row[0]].duration                        = row[3]
        RoomTraps[row[0]].playerdesc                      = str(row[4])
        RoomTraps[row[0]].roomdesc                        = str(row[5])

    return RoomTraps


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
        amRace.ClassList[row[0]].speed                           = row[10]

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
