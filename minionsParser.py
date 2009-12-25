#from twisted.internet.protocol import Protocol, Factory
#from twisted.protocols.basic import LineReceiver
#from twisted.internet import reactor
import minionDefines

import re, string


def commandParser(player, line):
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
    line = newline



    # Player isn't logged in yet, do dialog
    if player.STATUS != minionDefines.PLAYING:
        NotPlayingDialog(player, line)
        return

    cmd = line.split()
    if len(cmd) == 0:
        pass
    elif cmd[0].lower() == "/quit":
        player.disconnectClient()
    elif cmd[0].lower() == "users":
        player.sendLine(str(len(player.factory.players)) + " players connected.\r\n")
    elif cmd[0].lower() == "gos":
         cmdLen = len(cmd[0]) + 1
         player.Shout(minionDefines.MAGENTA + player.name + " gossips: " + line[cmdLen:] + minionDefines.WHITE )
    elif cmd[0].lower() == "who":
        player.sendToPlayer(minionDefines.CYAN + "<<=-=-=-=-= Whos Online =-=-=-=>>")
        for user in player.factory.players:
            player.sendToPlayer(minionDefines.CYAN + "  => " + minionDefines.MAGENTA + user.name)
        player.sendToPlayer(minionDefines.CYAN + "<<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>>")
    else:
        player.sendToRoom(minionDefines.GREEN + player.name + " says: " +minionDefines.WHITE + line)
        player.sendLine(minionDefines.GREEN + "You say: " + minionDefines.WHITE + line)


def NotPlayingDialog(player, line):

    if player.STATUS == minionDefines.GETNAME:
        line = line.split()
        name = line[0]
        player.name = name.capitalize()
        player.STATUS = minionDefines.GETPASSWORD
        player.transport.write("Enter your password: ")
        return
    elif player.STATUS == minionDefines.GETPASSWORD:
        player.Shout(player.name + " has joined.")
        player.STATUS = minionDefines.PLAYING
        player.sendToPlayer(minionDefines.LYELLOW + "Welcome " + player.name + "\r\n" )

        return

