import minionDefines, minionsCommands, minionsDB

import re, string


def commandParser(player, line):
    # Clean players input
    line = CleanPlayerInput(line)

    # Player isn't logged in yet, do dialog
    if player.STATUS != minionDefines.PLAYING:
        NotPlayingDialog(player, line)
        return

    cmd = line.split()
    if len(cmd) == 0: # or cmd[0] == chr(0x0D):
        pass
    elif cmd[0].lower() == "/quit":
        minionsCommands.Quit(player)
    elif cmd[0].lower() == "gos":
        minionsCommands.Gossip(player, line[(len(cmd[0]) + 1):])
    elif cmd[0].lower() == "who":
        minionsCommands.Who(player)
    elif cmd[0].lower() == "emote":       
        minionsCommands.Emote(player, line[(len(cmd[0]) + 1):])
    elif cmd[0].lower() == "help":
        minionsCommands.Help(player)
    else:  # Say it to the room
        minionsCommands.Say(player, line)

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
    elif player.STATUS == minionDefines.GETPASSWORD:
        GetPlayerPassword(player, line)
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
        player.STATUS = minionDefines.GETPASSWORD
        player.transport.write("Enter your password: ")
        return
        

###############################################
# GetPlayerPassword()
#
# Get player password at logon and log them in
###############################################
def GetPlayerPassword(player, line):
        player.Shout(minionDefines.BLUE + player.name + " has joined.")
        player.playerid = minionsDB.CreatePlayer(player)
        player.STATUS = minionDefines.PLAYING
        player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "!\r\nType 'help' for help" )
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
          pid = minionsDB.GetUserID(line)
          if pid != 0:
              player.playerid     = pid
              player.name         = line
              player.STATUS       = minionDefines.GETPASSWORD
              player.transport.write("Enter your password: ")
          else:
              player.transport.write("Player not found, hit Enter and try again.")
       else:
          player.STATUS           = minionDefines.GETNAME
          player.transport.write("Enter the name you would like to go by: ")