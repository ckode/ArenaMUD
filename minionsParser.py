#from twisted.internet.protocol import Protocol, Factory
#from twisted.protocols.basic import LineReceiver
#from twisted.internet import reactor
import minionDefines

import re, string


def commandParser(player, line):
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
        player.sendLine(str(len(player.factory.players)))
    else:
        player.sendToRoom(line)

        
def NotPlayingDialog(player, line):
    
    if player.STATUS == minionDefines.GETNAME:
        player.name = line
        player.STATUS = minionDefines.GETPASSWORD
        player.transport.write("Enter your password: ")
        return
    elif player.STATUS == minionDefines.GETPASSWORD:
        player.STATUS = minionDefines.PLAYING
        player.transport.write(minionDefines.LYELLOW + "Welcome " + player.name + "\r\n")
        player.factory.sendMessageToAllClients(player.name + " has joined.")
        return

