import minionDefines, minionsCommands, minionsDB
import minionsRooms

import re, string
from time import strftime, localtime

def printthis(line):
    print line
def printtwo(line, line2):
    print line + " " + line2

def commandParser(player, line):
    # Clean players input
    line = CleanPlayerInput(line)

    # Player isn't logged in yet, do dialog
    if player.STATUS != minionDefines.PLAYING:
        NotPlayingDialog(player, line)
        return

    # Map (dict) for commands to corosponding function
    commands = { '/quit':    minionsCommands.Quit,
                 'gossip':   minionsCommands.Gossip,
                 'emote':    minionsCommands.Emote,
                 'who':      minionsCommands.Who,
                 'set':      minionsCommands.Set,
                 'help':     minionsCommands.Help,
                 'look':     minionsCommands.Look,
                 'down':     minionsCommands.Down,
                 'up':       minionsCommands.Up,
                 'rofl':     minionsCommands.Rofl,
                 'wtf':      minionsCommands.Wtf
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
                commands[each](player)
                return
             continue
          elif each == "down":
             if len(cmd) == 1:
                commands[each](player)
                return
             continue
    # No command found so say it to the room
    minionsCommands.Say(player, line)
    return


#    if len(cmd) == 0: # or cmd[0] == chr(0x0D):
#        pass
#    elif cmd[0].lower() == "/quit":
#        minionsCommands.Quit(player)
#    elif cmd[0].lower() == "gos":
#        minionsCommands.Gossip(player, line[(len(cmd[0]) + 1):])
#    elif cmd[0].lower() == "who":
#        minionsCommands.Who(player)
#    elif cmd[0].lower() == "emote":       
#        minionsCommands.Emote(player, line[(len(cmd[0]) + 1):])
#    elif cmd[0].lower() == "help":
#        minionsCommands.Help(player)
#    elif cmd[0].lower() == "set":
#        minionsCommands.Set(player, line[(len(cmd[0]) + 1):])
#    else:  # Say it to the room
#        minionsCommands.Say(player, line)

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
    if line == minionsDB.GetPassword(player.name):
       minionsDB.LoadPlayer(player)
       player.Shout(minionDefines.BLUE + player.name + " has joined.")
       player.STATUS = minionDefines.PLAYING
       player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
       player.factory.players.append(player)
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
     if line == "":
        player.transport.write("Blank passwords not allowed, enter a password: ")
        return
     else:
        player.Shout(minionDefines.BLUE + player.name + " has joined.")
        player.password = line
        player.playerid = minionsDB.CreatePlayer(player)
        player.factory.players.append(player)
        player.STATUS = minionDefines.PLAYING
        player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
        player.factory.RoomList[player.room]
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
              player.playerid     = pid
              player.name         = name
              player.STATUS       = minionDefines.COMPAREPASSWORD
              player.transport.write("Enter your password: ")
          else:
              player.transport.write("Player not found, hit Enter and try again.")
       else:
          player.STATUS           = minionDefines.GETNAME
          player.transport.write("Enter the name you would like to go by: ")