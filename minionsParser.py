import minionDefines, minionsCommands

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
    else:  # Say it to the room
        minionsCommands.Say(player, line)

#############################################################
# CleanPlayerInput()
#
# Clean players input by removing all unprintable characters
# and properly applying deletes by backspacing
#############################################################
def CleanPlayerInput(line):
    # Remove all unprintable characters except BACKSPACE
    line = filter(lambda x: x in minionDefines.PRINTABLE_CHARS, line)
    #Delete characters before backspaces
    pos = 0
    lineSize = len(line)
    newline = ""
    for character in line:
       if character == chr(0x08):
          newline = newline[:-1]
       else:
          newline += character
    return newline

#############################################################
# NotPlayingDialog()
#
# This expedites all dialog when player isn't *playing*
#############################################################
def NotPlayingDialog(player, line):
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
        player.STATUS = minionDefines.PLAYING
        player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "\r\n" )
        return

