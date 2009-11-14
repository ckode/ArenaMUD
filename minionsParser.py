#from twisted.internet.protocol import Protocol, Factory
#from twisted.protocols.basic import LineReceiver
#from twisted.internet import reactor

import re, string


def commandParser(player, line):
    cmd = line.split()
    if cmd[0].lower() == "say":
        player.say(line)

    elif cmd[0].lower() == "/quit":
        player.disconnectClient()

    elif cmd[0].lower() == "users":
        player.sendLine(str(len(user.factory.users)))


