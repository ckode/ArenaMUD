from twisted.internet import reactor

import minionDefines, minionsCommands, minionsDB
import minionsRooms

import re, string
from time import strftime, localtime

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
                 'northeast':        minionsCommands.NorthEast,
                 'ne':               minionsCommands.NorthEast,
                 'east':             minionsCommands.East,
                 'southeast':        minionsCommands.SouthEast,
                 'se':               minionsCommands.SouthEast,
                 'south':            minionsCommands.South,
                 'southwest':        minionsCommands.SouthWest,
                 'sw':               minionsCommands.SouthWest,
                 'west':             minionsCommands.West,
                 'northwest':        minionsCommands.NorthWest,
                 'nw':               minionsCommands.NorthWest,
                 'rofl':             minionsCommands.Rofl,
                 'wtf':              minionsCommands.Wtf,
                 'slap':             minionsCommands.Slap
               }
    cmd = line.split()
    if len(cmd) == 0:
       minionsCommands.Look(player, player.room)
       return

    cmdstr = re.compile(re.escape(cmd[0].lower()))
    for each in commands.keys():
       if cmdstr.match(each):
          # Gossip command
          if each == "gossip":
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
          elif each == "up":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.Up, player)
                return
             continue
          elif each == "down":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.Down, player)
                return
             continue
          elif each == "north":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.North, player)
                return
             continue
          elif each == "northeast" and len(cmd[0]) == 6:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.NorthEast, player)
                return
             continue
          elif each == "ne" and len(cmd[0]) == 2:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.NorthEast, player)
                return
             continue
          elif each == "east":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.East, player)
                return
             continue
          elif each == "southeast" and len(cmd[0]) == 6:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.SouthEast, player)
                return
             continue
          elif each == "se" and len(cmd[0]) == 2:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.SouthEast, player)
                return
             continue
          elif each == "south":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.South, player)
                return
             continue
          elif each == "southwest" and len(cmd[0]) == 6:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.SouthWest, player)
                return
             continue
          elif each == "sw" and len(cmd[0]) == 2:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.SouthWest, player)
                return
             continue
          elif each == "west":
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.West, player)
                return
             continue
          elif each == "northwest" and len(cmd[0]) == 6:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.NorthWest, player)
                return
             continue
          elif each == "nw" and len(cmd[0]) == 2:
             if len(cmd) == 1:
                if player.moving == 1:
                   player.sendToPlayer(minionDefines.WHITE + "WAIT! You are already moving, slow down!!")
                   return
                player.moving = 1
                reactor.callLater(.5, minionsCommands.NorthWest, player)
                return
             continue
     # No command found so say it to the room
    minionsCommands.Say(player, line)
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
       print "Player's ID: " + str(player.playerid) + " Room: " + str(player.room)
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
def LoginPlayer(player, line):
    if line == "":
       player.transport.write('Enter your username or type "' + minionDefines.LYELLOW + 'new' + minionDefines.WHITE + '": ')
       return
    else:
       if line != "new":
          line = line.split()
          name = line[0]
          name = name.capitalize()
          pid = minionsDB.GetUserID(name)
          if pid > 0:
              if pid in player.factory.players.keys():
                 player.transport.write("Username is already connected!\r\n")
                 player.playerid = 0
                 player.disconnectClient()
                 return
              player.playerid     = pid
              player.name         = name
              player.STATUS       = minionDefines.COMPAREPASSWORD
              player.transport.write("Enter your password: ")
          else:
              player.transport.write("Player not found, hit Enter and try again.")
       else:
          player.STATUS           = minionDefines.GETNAME
          player.transport.write("Enter the name you would like to go by: ")