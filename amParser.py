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

import amDefines, amCommands, amDB, amMaps, amSocial
import amRooms, amUtils, amRace, amSpells, amHelp

import re, string
from time import strftime, localtime

USERPID = 1
FULLDESC = 0

# Map (dict) for commands to corosponding function
commands = { '/quit':            amCommands.Quit,
             'gossip':           amCommands.Gossip,
             'emote':            amCommands.Emote,
             'who':              amCommands.WhoCmd,
             'set':              amCommands.Set,
             'help':             amHelp.HelpParser,
             'look':             amCommands.Look,
             'down':             amCommands.Down,
             'up':               amCommands.Up,
             'north':            amCommands.North,
             'ne':               amCommands.NorthEast,
             'east':             amCommands.East,
             'se':               amCommands.SouthEast,
             'south':            amCommands.South,
             'sw':               amCommands.SouthWest,
             'west':             amCommands.West,
             'nw':               amCommands.NorthWest,
             'crackpipe':        amCommands.Crackpipe,
             'rofl':             amCommands.Rofl,
             'wtf':              amCommands.Wtf,
             'slap':             amCommands.Slap,
             'vision':           "",
             'brief':            amCommands.Brief,
             'open':             amCommands.Open,
             'close':            amCommands.Close,
             'remote':           "",
             'look':             amCommands.LookAt,
             'bash':             amCommands.Bash,
             'superuser':        "",
             'attack':           amCommands.Attack,
             'rest':             amCommands.Rest,
             'sneak':            amCommands.Sneak,
             'break':            amCommands.Break,
             'nextmap':          amCommands.NextMap,
             'status':           amCommands.Status,
             'spells':           amCommands.ListSpells,
             'reroll':           amCommands.Reroll,
             'get':              amCommands.Get,
             'statline':         "",
}

def commandParser(player, line):

    # If player is stun, do nothing
    if player.stun:
        player.sendToPlayer("You stare blankly.")
        player.sendToRoomNotVictim( player.playerid, "%s%s stares blankly!" % (amDefines.YELLOW, player.name) )
        return
    # Clean players input
    line = CleanPlayerInput(line)
    

    # Player isn't logged in yet, do dialog
    if player.STATUS != amDefines.PLAYING:
        NotPlayingDialog(player, line)
        return

    cmd = line.split()
    # Player just hit enter, look around the room.
    if len(cmd) == 0:
        amCommands.Look(player, player.room, player.briefDesc)
        return

    # Is the command a spell?
    if cmd[0] in amSpells.SpellList.keys():
        if not amCommands.CastSpell( player, cmd ):
            amCommands.Say(player, line)
            player.sneaking = False
            return
        return

    # Is the command a social action?
    if cmd[0] in amSocial.SocalList.keys():
        pass
        
    cmdstr = re.compile(re.escape(cmd[0].lower()))
    for each in commands.keys():
        if cmdstr.match(each):
           # TESTING, REMOVE VISION OPTION WHEN DONE!
            if each == "vision":
                if player.isAdmin:
                    if len(cmd[0]) > 4:
                       #if cmd[1] == 1 or cmd[1] == 2 or cmd[1] == 3:
                        player.vision = int(cmd[1])
                        player.sendToPlayer("%sVision changed." % (amDefines.WHITE,) )
                        return
                    continue       
            elif each == "rest":
                if len(cmd[0]) == 4 and len(cmd) == 1:
                    commands[each](player)
                    return
            elif each == "break":
                if len(cmd[0]) > 1 and len(cmd) == 1:
                    commands[each](player)
                    return
            # Become an admin (access admin commands)
            elif each == "superuser":
                if len(cmd) == 2:
                    Superuser(player, line[(len(cmd[0]) + 1):])
                    return
                elif len(cmd[0]) != 1:
                    amUtils.StatLine(player)
                    return
            # Attack someone!
            elif each == "attack":
                if len(cmd) == 2:
                    amCommands.Attack(player, line[(len(cmd[0]) + 1):])
                    return
            # Get item
            elif each == "get":
                if len(cmd) == 2:
                    amCommands.Get(player, line[(len(cmd[0]) + 1):])
                    return
            # Look
            elif each == "look":
                # if nothing to look at supplied, just look around the room
                if len(cmd) == 1:
                    amCommands.Look(player, player.room, FULLDESC )
                    return
                # If it's 2, that means it's not a sentence we are looking at something
                elif len(cmd) == 2:
                    # Call LookAt() to determine what they are looking at
                    commands[each](player, line[(len(cmd[0]) + 1):])
                    return
                continue
            # Open Command (open doors etc)
            elif each == "open":
                if len(cmd) > 1 and len(cmd) > 1:
                    commands[each](player, line[(len(cmd[0]) + 1):])
                    return
                continue
            # Close Command (open doors etc)
            elif each == "close":
                if len(cmd) > 1 and len(cmd) > 1:
                    commands[each](player, line[(len(cmd[0]) + 1):])
                    return
                continue
            # bash Command (open doors etc)
            elif each == "bash":
                if len(cmd) > 1 and len(cmd) > 1:
                    commands[each](player, line[(len(cmd[0]) + 1):])
                    return
                continue
            # Call next map
            elif each == "nextmap":
                if len(cmd[0]) == 7 and len(cmd) == 1:
                    if player.isAdmin:
                        commands[each](player)
                        return
            # Brief command (for brief room desc)
            elif each == "brief":
                if len(cmd[0]) == 5 and len(cmd) == 1:
                    commands[each](player)
                    return
            # Gossip command
            elif each == "gossip":
                if len(cmd[0]) > 2 and len(cmd) > 1:
                    commands[each](player, line[(len(cmd[0]) + 1):])
                    return
                continue
            # Slap someone!
            elif each == "slap":
                if len(cmd[0]) == 4:
                    if len(cmd) > 1:
                        amCommands.Slap(player, cmd[1])
                    else:
                        amCommands.Slap(player, "")
                    return
                continue
            # Who command (who typed by itself)
            elif each == "who":
                if len(cmd[0]) == 3 and len(cmd) == 1:
                    commands[each](player)
                    return
                continue
            # Emote command
            elif each == "emote":
                if len(cmd[0]) > 2 and len(cmd) > 1:
                    commands[each](player, line[(len(cmd[0]) + 1):])
                    return
                continue
            # Remote command
            elif each == "remote":
                if player.isAdmin:
                    if len(cmd[0]) > 2 and len(cmd) > 2:
                        for user in player.factory.players.values():
                            if user.name == cmd[1].capitalize():
                                commandParser(user, line[(len(cmd[0]) + len(cmd[1]) + 2):])
                        return
                    continue
            # Help command (help typed by itself)
            elif each == "help":
                if len(cmd[0]) == 4:
                    if len(cmd) > 2:
                        continue
                    elif len(cmd) > 1:
                        commands[each](player, cmd[1])
                    else:
                        amHelp.GeneralHelpTopics(player)
                    return
                continue
            # Set command
            elif each == "set":
                if len(cmd[0]) == 3:
                    commands[each](player, line[(len(cmd[0]) + 1):])
                    return
                continue
            elif each == "look":
                if len(cmd) == 1:
                    commands[each](player, player.room)
                    return
            # Quit command
            elif each == "/quit":
                if len(cmd[0]) > 1:
                    commands[each](player)
                    return
                continue
            elif each == "rofl":
                if len(cmd) == 1 and len(cmd[0]) == 4:
                    commands[each](player)
                    return
                continue
            elif each == "crackpipe":
                if len(cmd) == 1 and len(cmd[0]) > 4:
                    commands[each](player)
                    return
                continue
            elif each == "wtf":
                if len(cmd) == 1 and len(cmd[0]) == 3:
                    commands[each](player)
                    return
                continue
            elif each == "sneak":
                if len(cmd) == 1 and len(cmd[0]) > 1:
                    commands[each](player)
                    return
                continue
            elif each == "up":
                if len(cmd) == 1:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.Up, player)
                    return
                continue
            elif each == "down":
                if len(cmd) == 1:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.Down, player)
                    return
                continue
            elif each == "north":
                if len(cmd) == 1 and len(cmd[0]) != 2:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.North, player)
                    return
                continue
            elif each == "ne" and len(cmd[0]) == 2:
                if len(cmd) == 1:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.NorthEast, player)
                    return
                continue
            elif each == "east":
                if len(cmd) == 1:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.East, player)
                    return
                continue
            elif each == "south":
                if len(cmd) == 1 and len(cmd[0]) != 2:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.South, player)
                    return
                continue
            elif each == "se" and len(cmd[0]) == 2:
                if len(cmd) == 1:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.SouthEast, player)
                    return
                continue
            elif each == "sw" and len(cmd[0]) == 2:
                if len(cmd) == 1:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.SouthWest, player)
                    return
                continue
            elif each == "west":
                if len(cmd) == 1:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.West, player)
                    return
                continue
            elif each == "nw" and len(cmd[0]) == 2:
                if len(cmd) == 1:
                    if player.moving == 1:
                        player.sendToPlayer(amDefines.WHITE + "WAIT! You are already moving, slow down!!")
                        return
                    if player.sneaking:
                        player.sendToPlayer("Sneaking...")
                    player.moving = 1
                    reactor.callLater(.5, amCommands.NorthWest, player)
                    return
                continue
            elif each == "status":
                if len(cmd) == 1 and len(cmd[0]) > 1:
                    commands[each](player)
                    return
                continue
            elif each == "spells":
                if len(cmd) == 1 and len(cmd[0]) > 1:
                    commands[each](player)
                    return
                continue
            elif each == "reroll":
                if len(cmd) == 1 and len(cmd[0]) > 4:
                    commands[each](player)
                    return
                continue
            elif each == "statline":
                if len(cmd) == 2 and len(cmd[0]) == 8 and cmd[1] == "off":
                    player.statLine = False
                    return
                elif len(cmd) == 2 and len(cmd[0]) == 8 and cmd[1] == "on":
                    player.statLine = True
                    return
                                

    # No command found so say it to the room
    amCommands.Say(player, line)
    player.sneaking = False
    return



#############################################################
# CleanPlayerInput()
#
# Clean players input by removing all unprintable characters
# and properly applying deletes by backspacing
#############################################################
def CleanPlayerInput(line):
    #Delete characters before backspaces
    pos = 0
    lineSize = len(line)
    newline = ""
    for character in line:
        if character == chr(0x08):
            newline = newline[:-1]
        else:
            newline += character
    # Remove all unprintable characters
    line = filter(lambda x: x in string.printable, newline)
    return line

#############################################################
# NotPlayingDialog()
#
# This expedites all dialog when player isn't *playing*
#############################################################
def NotPlayingDialog(player, line):
    if player.STATUS == amDefines.LOGIN:
        LoginPlayer(player, line)
        return
    # Get player login name
    if player.STATUS == amDefines.GETNAME:
        GetPlayerName(player, line)
        return
    # Get player password
    elif player.STATUS == amDefines.COMPAREPASSWORD:
        ComparePassword(player, line)
        return
    elif player.STATUS == amDefines.GETPASSWORD:
        SetPassword(player, line)
        return
    elif player.STATUS == amDefines.GETCLASS:
        PickClass(player, line)
        return
    elif player.STATUS == amDefines.GETRACE:
        PickRace(player, line)
        return
    elif player.STATUS == amDefines.PURGATORY:
        PurgatoryParser(player, line)
        return


###############################################
# GetPlayerName()
#
# Get player name at logon and ask for password
###############################################
def GetPlayerName(player, line):
    line = line.split()
    name = line[0]
    player.name = name.capitalize()
    pid = amDB.GetUserID(player.name)
    if pid > 0:
        player.transport.write("Username already exists, try again: ")
    else:
        player.STATUS = amDefines.GETPASSWORD
        player.transport.write("Enter your password: ")
    return


###############################################
# ComparePassword()
#
# Get player password at logon and log them in
###############################################
def ComparePassword(player, line):
    global RoomList

    if line == amDB.GetPassword(player.name):
        amDB.LoadPlayer(player)
        player.Shout(amDefines.BLUE + player.name + " has joined.")
        player.STATUS = amDefines.PLAYING
        player.sendToPlayer(amDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
        player.factory.players[player.playerid] = player
        # Put player in current room
        player.room = 1
        amMaps.Map.Rooms[player.room].Players[player.playerid] = player.name
        amCommands.Look(player, player.room, player.briefDesc)
        print strftime("%b %d %Y %H:%M:%S ", localtime()) + player.name + " just logged on."
        return
    else:
        player.transport.write("Incorrect password, enter a password: ")

###############################################
# SetPassword()
#
# Sets new player's password
###############################################
def SetPassword(player, line):
    global RoomList

    if line == "":
        player.transport.write("Blank passwords not allowed, enter a password: ")
        return
    else:
        player.Shout(amDefines.BLUE + player.name + " has joined.")
        player.password = line
        player.playerid = amDB.CreatePlayer(player)
        player.factory.players[player.playerid] = player
        # Put player in current room
        amMaps.Map.Rooms[player.room].Players[player.playerid] = player.name
        player.STATUS = amDefines.PLAYING
        player.sendToPlayer(amDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
        amCommands.Look(player, player.room, briefDesc)
        print strftime("%b %d %Y %H:%M:%S ", localtime()) + player.name + " created an account and logged on."
        return
###############################################
# LoginPlayer()
#
# Ask for username or new
###############################################
def  LoginPlayer(player, line):
    global USERPID
    global AnsiScreen

    if line == "":
        player.transport.write(amRooms.AnsiScreen)
        player.transport.write('Enter your warriors name: ')
        return
    else:
        line = line.split()
        name = line[0]
        #limit the name to a reasonable length
        if len(name) > 15:
            player.transport.write(amDefines.DEFAULT + "Name is limited to 15 characters, try again.\r\n" + amDefines.WHITE)
            player.STATUS = amDefines.LOGIN
            player.transport.write("Enter your warriors name: ")            
            return
        #name should now be 15 or less characters in length
        name = name.capitalize()
        for each in player.factory.players.keys():
            if player.factory.players[each].name == name:
                player.transport.write("That warrior is already in the arena!\r\n")
                player.STATUS           = amDefines.LOGIN
                player.transport.write("Enter a different warrior name: ")
                return

        player.playerid     = USERPID
        USERPID += 1
        player.name         = name
        player.STATUS       = amDefines.GETCLASS
        player.transport.write("Choose a class:\r\n")
        for cid, cname in amRace.ClassList.items():
            player.transport.write( "   %s. %s\r\n" % (cid, cname.name) )
        player.transport.write("Select: ")
        return

################################################
# PickClass
################################################
def PickClass(player, classnum):
    # Sub fuction to display the Class menu
    def DisplayChoices():
        player.transport.write("Choose a class:\r\n")
        for cid, cname in amRace.ClassList.items():
            player.transport.write( "   %s. %s\r\n" % (cid, cname.name) )
        player.transport.write("Select: ")

    # If an invalid choice was made, tell them
    def InvalidChoice():
        player.transport.write("Invalid choice, please try again.\r\n")

    # Redisplay classes if no option was selected
    if classnum == "":
        DisplayChoices()
        return
    
    # Make sure the entered option is numeric
    try: 
        classnum = int(classnum)
    except:
        InvalidChoice()
        DisplayChoices()
        return
    
    if classnum in amRace.ClassList.keys():
        playerclass             = amRace.ClassList[classnum]
        player.Class            = classnum
        player.hp               = playerclass.hpbonus
        player.maxhp            = player.hp
        player.mindamage        = playerclass.mindamage
        player.maxdamage        = playerclass.maxdamage
        player.magery           = playerclass.MageryType
        # If class has stealth, then player can sneak
        if playerclass.stealth > 0:
            player.ClassStealth = True
        player.stealth         += playerclass.stealth
        player.weapontext       = playerclass.weapontext
        player.STATUS           = amDefines.GETRACE
        player.speed            = playerclass.speed
        player.offense          = playerclass.Offense
        player.defense          = playerclass.Defense
        player.spellcasting     = playerclass.Spellcasting
        player.magicres         = playerclass.MR

        # Now display race choices
        player.transport.write("Choose a race:\r\n")
        for rid, rname in amRace.RaceList.items():
            player.transport.write( "   %s. %s\r\n" % (rid, rname.name) )
        player.transport.write("Select: ")
    else:
        InvalidChoice()
        DisplayChoices()
    return

################################################
# PickRace
################################################
def PickRace(player, racenum):
    # Sub fuction to display the Race menu
    def DisplayChoices():
        player.transport.write("Choose a race:\r\n")
        for rid, rname in amRace.RaceList.items():
            player.transport.write( "   %s. %s\r\n" % (rid, rname.name) )
        player.transport.write("Select: ")

    # If an invalid choice was made, tell them
    def InvalidChoice():
        player.transport.write("Invalid choice, please try again.\r\n")
        
    # Redisplay races if no option was selected
    if racenum == "":
        DisplayChoices()
        return
    
    # Make sure the entered option is numeric
    try:
        racenum = int(racenum)
    except:
        InvalidChoice()
        DisplayChoices()
        return
    
    if racenum in amRace.RaceList.keys():
        race                    = amRace.RaceList[racenum]
        player.race             = racenum
        player.hp              += race.basehp
        player.maxhp            = player.hp
        player.mindamage       += race.damagebonus
        player.maxdamage       += race.damagebonus
        player.offense         += race.attackbonus
        player.spellcasting    += race.castingbonus
        player.vision           = race.vision
        player.stealth         += race.stealth
        player.STATUS           = amDefines.PLAYING
        player.staticmaxhp      = player.maxhp
        player.magicres        += race.MRBonus
        player.speed           += race.SpeedBonus

        if player.Rerolling == False:
            print strftime("%b %d %Y %H:%M:%S ", localtime()) + player.name + " just logged on."
            player.Shout("%sA %s %s named %s has joined." % (amDefines.BLUE, race.name, amRace.ClassList[player.Class].name, player.name) )
            player.sendToPlayer(amDefines.YELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
            player.sendToPlayer("%s>> Current Map: %s%s" % (amDefines.GREEN, amDefines.LCYAN, amMaps.Map.MapInfo[0]) )
            player.factory.players[player.playerid] = player
        else:
            player.Shout("%s%s has rerolled into a %s %s." % (amDefines.BLUE, player.name, race.name, amRace.ClassList[player.Class].name) )
            player.Rerolling = False

        amUtils.EnterPurgatory(player)
    else:
        InvalidChoice()
        DisplayChoices()
    return

#############################################
# Superuser command (move this to commands?)
#############################################
def Superuser(player, password):
    if password == "digital":
        player.isAdmin = True
        amUtils.StatLine(player)


##############################################
# PurgatoryParser()
#
# Command parser for when the player is in purgatory (ie, logged in, but not playing)
##############################################
def PurgatoryParser(player, line):
    commands = { '/quit':            amCommands.Quit,
                 'gossip':           amCommands.Gossip,
                 'spawn':            amUtils.SpawnPlayer,
                 'who':              amCommands.Who,
                 'help':             amHelp.HelpParser,
                 'superuser':        "",
                 'nextmap':          amCommands.NextMap,
                 'reroll':           amCommands.Reroll
               }

    cmd = line.split()
    # Player just hit enter, look around the room.
    if len(cmd) == 0:
        amUtils.StatLine(player)
        return

    cmdstr = re.compile(re.escape(cmd[0].lower()))
    for each in commands.keys():
        if cmdstr.match(each):
            if each == "gossip":
                if len(cmd[0]) > 2 and len(cmd) > 1:
                    commands[each](player, line[(len(cmd[0]) + 1):])
                    return
                continue
            elif each == "/quit":
                if len(cmd[0]) > 1:
                    commands[each](player)
                    
                    return
                continue
            # Call next map
            elif each == "nextmap":
                if len(cmd[0]) == 7 and len(cmd) == 1:
                    if player.isAdmin:
                        commands[each](player)
                        return
            elif each == "spawn":
                if len(cmd[0]) > 2 and len(cmd) == 1:
                    amUtils.SpawnPlayer(player)
                    return
                continue
            # Who command (who typed by itself)
            elif each == "who":
                if len(cmd[0]) == 3 and len(cmd) == 1:
                    commands[each](player)
                    return
                continue
           # Help command (help typed by itself)
            elif each == "help":
                if len(cmd) > 1:
                    commands[each](player, cmd[1])
                    return
                else:
                    amHelp.GeneralHelpTopics(player)
                    return
                continue
            # Become an admin (access admin commands)
            elif each == "superuser":
                if len(cmd) == 2:
                    Superuser(player, line[(len(cmd[0]) + 1):])
                    return
                elif len(cmd[0]) != 1:
                    return
            elif each == "reroll":
                if len(cmd) == 1 and len(cmd[0]) > 4:
                    commands[each](player)
                    return
                continue
                
    player.sendToPlayer("Command had no effect. Type 'spawn' to spawn or type 'help' for help.")