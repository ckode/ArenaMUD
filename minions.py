from twisted.internet.protocol import ServerFactory
from twisted.internet import defer
from twisted.python import failure, util
from twisted.internet import reactor
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol

import minionsParser, minionsPlayer, minionDefines, minionsLog
import minionsRooms, minionsDB

import sys 
from time import strftime, localtime


class Users(StatefulTelnetProtocol):
    playerid           = None
    name               = ""
    lastname           = ""
    password           = ""
    strength           = 0
    agility            = 0
    intelligence       = 0
    wisdom             = 0
    charm              = 0
    health             = 0
    hp                 = 0
    mana               = 0
    mr                 = 0
    stealth            = 0
    weight             = 0
    room               = 1
    holding            = {}
    wearing            = { 'arms':         None,
                           'head':         None,
                           'torso':        None,
                           'l_finger':     None,
                           'r_finger':     None,
                           'legs':         None,
                           'neck':         None,
                           'feet':         None
                         }


    def connectionMade(self):
        

        # Limit how many can connect at one time
        if len(self.factory.players) > 10:
            self.transport.write("Too many connections, try later")
            self.disconnectClient()
        self.STATUS = minionDefines.LOGIN
        minionsParser.LoginPlayer(self, "")



    def disconnectClient(self):
        self.sendLine("Goodbye")
        self.factory.players.remove(self)
        self.factory.sendMessageToAllClients(minionDefines.BLUE + self.name + " just logged off.")
        print strftime("%b %d %Y %H:%M:%S ", localtime()) + self.name + " just logged off."
        self.transport.loseConnection()

    def connectionLost(self, reason):
        # If player hungup, disconnectClient() didn't remove the user, remove them now
        if self in self.factory.players:
            self.factory.players.remove(self)
        if self.name != "":
            self.factory.sendMessageToAllClients(minionDefines.BLUE + self.name + " just hung up!")
            print strftime("%b %d %Y %H:%M:%S ", localtime()) + self.name + " just hung up!."

    def lineReceived(self, line):
        minionsParser.commandParser(self, line)
        #self.say(line)


    def say(self, line):
        self.sendToPlayer("You say, " + line)

    def sendToPlayer(self, line):
        self.sendLine(line + minionDefines.WHITE)

    ################################################
    # Send to everyone in current room
    ################################################
    def sendToRoom(self, line):
        for player in self.factory.players:
            if player == self and player.STATUS == minionDefines.PLAYING:
                pass #self.say(line)
            else:
                if player.STATUS == minionDefines.PLAYING:
                    player.sendToPlayer(line + minionDefines.WHITE)
                    
    ################################################
    # Shout to everyone                            #
    ################################################
    def Shout(self, line):
        for player in self.factory.players:
           if player.STATUS == minionDefines.PLAYING:
               player.sendToPlayer(line + minionDefines.WHITE)


    def Shutdown(self):
        self.reactor.stop()
        #sys.exit()





class SonzoFactory(ServerFactory):
    def __init__(self):
        self.players = []
        self.RoomList = {}
        minionsDB.LoadRooms(self)
 
    def sendMessageToAllClients(self, mesg):
        for client in self.players:
            if client.STATUS == minionDefines.PLAYING:
                client.sendLine(mesg + minionDefines.WHITE)




#Create server factory
factory = SonzoFactory()
# Start listener on port 23 (telnet)
factory.protocol = lambda: TelnetTransport(Users)
reactor.listenTCP(23, factory)
reactor.run()