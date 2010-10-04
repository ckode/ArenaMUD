from twisted.internet import reactor

import minionDefines, minionsCommands, minionsDB
import minionsRooms, minionsUtils, minionsRace

import re, string
from time import strftime, localtime

USERPID = 1

def commandParser(player, line):

    # Clean players input
    line = CleanPlayerInput(line)

    # Player isn't logged in yet, do dialog
    if player.STATUS != minionDefines.PLAYING:
        NotPlayingDialog(player, line)
        return
    # Map (dict) for commands to corosponding function
    commands = { '/quit':            minionsCommands.Quit,
                 'gossip':           minionsCommands.Gossip,
                 'emote':            minionsCommands.Emote,
                 'who':              minionsCommands.Who,
                 'set':              minionsCommands.Set,
                 'help':             minionsCommands.Help,
                 'look':             minionsCommands.Look,
                 'down':             minionsCommands.Down,
                 'up':               minionsCommands.Up,
                 'north':            minionsCommands.North,
                 'ne':               minionsCommands.NorthEast,
                 'east':             minionsCommands.East,
                 'se':               minionsCommands.SouthEast,
                 'south':            minionsCommands.South,
                 'sw':               minionsCommands.SouthWest,
                 'west':             minionsCommands.West,
                 'nw':               minionsCommands.NorthWest,
                 'rofl':             minionsCommands.Rofl,
                 'wtf':              minionsCommands.Wtf,
                 'slap':             minionsCommands.Slap,
                 'vision':           "",
                 'brief':            minionsCommands.Brief,
                 'open':             minionsCommands.Open,
                 'close':            minionsCommands.Close,
                 'remote':           "",
                 'look':             minionsCommands.LookAt,
                 'bash':             minionsCommands.Bash,
                 'superuser':        "",
                 'attack':           minionsCommands.Attack,
                 'rest':             "",
                 'sneak':            minionsCommands.Sneak
               }
    cmd = line.split()
    # Player just hit enter, look around the room.
    if len(cmd) == 0:
       minionsCommands.Look(player, player.room)
       return

    cmdstr = re.compile(re.escape(cmd[0].lower()))
    for each in commands.keys():
       if cmdstr.match(each):
          # TESTING, REMOVE VISION OPTION WHEN DONE!
          if each == "vision":
              if player.isAdmin == True:
                if len(cmd[0]) > 4:
                   #if cmd[1] == 1 or cmd[1] == 2 or cmd[1] == 3:
                   player.vision = int(cmd[1])
                   player.sendToPlayer("%sVision changed." % (minionDefines.WHITE,) )
                   return
                continue
          elif each == "rest":
             if len(cmd[0]) > 2:
                player.resting = True
                player.sendToPlayer("%sYou are now resting." % (minionDefines.WHITE,))
                return
          # Become an admin (access admin commands)
          elif each == "superuser":
             if len(cmd) == 2:
                Superuser(player, line[(len(cmd[0]) + 1):])
                return
             elif len(cmd[0]) != 1:
                minionsUtils.StatLine(player)
                return
          # Attack someone!
          elif each == "attack":
             if len(cmd) == 2:
                minionsCommands.Attack(player, line[(len(cmd[0]) + 1):])
                return
          # Look
          elif each == "look":
             # if nothing to look at supplied, just look around the room
             if len(cmd) == 1:
                minionsCommands.Look(player, player.room)
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
                #player.sendToPlayer("%s%s" % (minionDefines.WHITE, "Command disabled.") )
                #return
                commands[each](player, line[(len(cmd[0]) + 1):])
                return
             continue
          # Close Command (open doors etc)
          elif each == "close":
             if len(cmd) > 1 and len(cmd) > 1:
                #player.sendToPlayer("%s%s" % (minionDefines.WHITE, "Command disabled.") )
                #return
                commands[each](player, line[(len(cmd[0]) + 1):])
                return
             continue
          # bash Command (open doors etc)
          elif each == "bash":
             if len(cmd) > 1 and len(cmd) > 1:
                commands[each](player, line[(len(cmd[0]) + 1):])
                return
             continue
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
                   minionsCommands.Slap(player, cmd[1])
                else:
                   minionsCommands.Slap(player, "")
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
             if player.isAdmin == True:
                if len(cmd[0]) > 2 and len(cmd) > 2:
                   for user in player.factory.players.values():
                       if user.name == cmd[1].capitalize():
                          commandParser(user, line[(len(cmd[0]) + len(cmd[1]) + 2):])
                   return
                continue
          # Help command (help typed by itself)
          elif each == "help":
             if len(cmd) == 1 and len(cmd[0]) == 4:
                commands[each](player)
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
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.Up, player)
                return
             continue
          elif each == "down":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.Down, player)
                return
             continue
          elif each == "north":
             if len(cmd) == 1 and len(cmd[0]) != 2:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.North, player)
                return
             continue
          elif each == "ne" and len(cmd[0]) == 2:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.NorthEast, player)
                return
             continue
          elif each == "east":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.East, player)
                return
             continue
          elif each == "south":
             if len(cmd) == 1 and len(cmd[0]) != 2:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.South, player)
                return
             continue
          elif each == "se" and len(cmd[0]) == 2:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.SouthEast, player)
                return
             continue
          elif each == "sw" and len(cmd[0]) == 2:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.SouthWest, player)
                return
             continue
          elif each == "west":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.West, player)
                return
             continue
          elif each == "nw" and len(cmd[0]) == 2:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                if player.sneaking:
                    player.sendToPlayer("Sneaking...")
                player.moving = 1
                reactor.callLater(.5, minionsCommands.NorthWest, player)
                return
             continue
#       elif minionsRooms.RoomList[player.room].SecretDirection > 0:
#          if line.lower() == minionsRooms.RoomList[player.room].SecretPhrase.lower():
#             RoomID = player.room
#             minionsUtils.ToggleSecretExit(RoomID, True)
#
#             if minionsRooms.RoomList[player.room].ActionID > 0:
#                minionsUtils.DisplayAction(player, minionsRooms.RoomList[player.room].ActionID)
#             reactor.callLater( 120, minionsUtils.ToggleSecretExit, RoomID, False)
#             return



     # No command found so say it to the room
    minionsCommands.Say(player, line)
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
    if player.STATUS == minionDefines.LOGIN:
        LoginPlayer(player, line)
        return
    # Get player login name
    if player.STATUS == minionDefines.GETNAME:
        GetPlayerName(player, line)
        return
    # Get player password
    elif player.STATUS == minionDefines.COMPAREPASSWORD:
        ComparePassword(player, line)
        return
    elif player.STATUS == minionDefines.GETPASSWORD:
        SetPassword(player, line)
        return
    elif player.STATUS == minionDefines.GETCLASS:
        PickClass(player, line)
        return
    elif player.STATUS == minionDefines.GETRACE:
        PickRace(player, line)
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
    pid = minionsDB.GetUserID(player.name)
    if pid > 0:
       player.transport.write("Username already exist, try again: ")
    else:
       player.STATUS = minionDefines.GETPASSWORD
       player.transport.write("Enter your password: ")
    return


###############################################
# ComparePassword()
#
# Get player password at logon and log them in
###############################################
def ComparePassword(player, line):
    global RoomList

    if line == minionsDB.GetPassword(player.name):
       minionsDB.LoadPlayer(player)
       player.Shout(minionDefines.BLUE + player.name + " has joined.")
       player.STATUS = minionDefines.PLAYING
       player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
       player.factory.players[player.playerid] = player
       # Put player in current room
       player.room = 1
       minionsRooms.RoomList[player.room].Players[player.playerid] = player.name
       minionsCommands.Look(player, player.room)
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
        player.Shout(minionDefines.BLUE + player.name + " has joined.")
        player.password = line
        player.playerid = minionsDB.CreatePlayer(player)
        player.factory.players[player.playerid] = player
        # Put player in current room
        minionsRooms.RoomList[player.room].Players[player.playerid] = player.name
        player.STATUS = minionDefines.PLAYING
        player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
        minionsCommands.Look(player, player.room)
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
       player.transport.write(minionsRooms.AnsiScreen)
       player.transport.write('Enter your warriors name: ')
       return
    else:
       line = line.split()
       name = line[0]
       name = name.capitalize()
       for each in player.factory.players.keys():
          if player.factory.players[each].name == name:
              player.transport.write("That warrior is already in the arena!\r\n")
              player.STATUS           = minionDefines.LOGIN
              player.transport.write("Enter a different warrior name: ")
              return

       player.playerid     = USERPID
       USERPID += 1
       player.name         = name
       player.STATUS       = minionDefines.GETCLASS
       player.transport.write("Choose a class:\r\n")
       for cid, cname in minionsRace.ClassList.items():
          player.transport.write( "   %s. %s\r\n" % (cid, cname.name) )
       player.transport.write("Select: ")
       return
   ##########################
       player.Shout(minionDefines.BLUE + player.name + " has joined.")
       player.STATUS = minionDefines.PLAYING
       player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
       player.factory.players[player.playerid] = player
       # Put player in current room
       player.room = 1
       minionsRooms.RoomList[player.room].Players[player.playerid] = player.name
       minionsCommands.Look(player, player.room)
       print strftime("%b %d %Y %H:%M:%S ", localtime()) + player.name + " just logged on."
       return

################################################
# PickClass
################################################
def PickClass(player, classnum):
    def DisplayChoices():
       player.transport.write("Choose a class:\r\n")
       for cid, cname in minionsRace.ClassList.items():
          player.transport.write( "   %s. %s\r\n" % (cid, cname.name) )
       player.transport.write("Select: ")
    if classnum == "":
        DisplayChoices()
        return
    classnum = int(classnum)
    if classnum in minionsRace.ClassList.keys():
        playerclass             = minionsRace.ClassList[classnum]
        player.Class            = classnum
        player.hp               = playerclass.hpbonus
        player.maxhp            = player.hp
        player.mindamage       += playerclass.mindamage
        player.maxdamage       += playerclass.maxdamage
        player.ac              += playerclass.BaseArmor
        player.magery           = playerclass.MageryType
        # If class has stealth, then player can sneak
        if playerclass.stealth > 0:
            player.ClassStealth = True
        player.stealth         += playerclass.stealth
        player.weapontext       = playerclass.weapontext
        player.STATUS           = minionDefines.GETRACE

        # Now display race choices
        player.transport.write("Choose a race:\r\n")
        for rid, rname in minionsRace.RaceList.items():
           player.transport.write( "   %s. %s\r\n" % (rid, rname.name) )
        player.transport.write("Select: ")
    else:
        player.transport.write("Invalid choice, please try again.\r\n")
        DisplayChoices()
    return

################################################
# PickRace
################################################
def PickRace(player, racenum):
    def DisplayChoices():
       player.transport.write("Choose a race:\r\n")
       for rid, rname in minionsRace.RaceList.items():
          player.transport.write( "   %s. %s\r\n" % (rid, rname.name) )
       player.transport.write("Select: ")
    if racenum == "":
        DisplayChoices()
        return
    racenum = int(racenum)
    if racenum in minionsRace.RaceList.keys():
        race                    = minionsRace.RaceList[racenum]
        player.race             = racenum
        player.hp              += race.basehp
        player.maxhp            = player.hp
        player.mindamage       += race.damagebonus
        player.maxdamage       += race.damagebonus
        player.ac              += race.defensebonus
        player.attackroll      += race.attackbonus
        player.spellcasting    += race.castingbonus
        player.vision           = race.vision
        player.stealth         += race.stealth
        player.STATUS           = minionDefines.PLAYING

        player.Shout(minionDefines.BLUE + player.name + " has joined.")
        player.STATUS = minionDefines.PLAYING
        player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
        player.factory.players[player.playerid] = player
        # Put player in current room
        player.room = 1
        minionsRooms.RoomList[player.room].Players[player.playerid] = player.name
        minionsCommands.Look(player, player.room)
        print strftime("%b %d %Y %H:%M:%S ", localtime()) + player.name + " just logged on."
    else:
       player.transport.write("Invalid choice, please try again.\r\n")
       DisplayChoices()
    return

#############################################
# Superuser command (move this to commands?)
#############################################
def Superuser(player, password):
    if password == "digital":
        player.isAdmin = True
        minionsUtils.StatLine(player)