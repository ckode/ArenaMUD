from twisted.internet.protocol import ServerFactory
from twisted.internet import defer
# Twisted specific imports
from twisted.python import failure, util
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol

# Minions specific imports
import minionsParser, minionsPlayer, minionDefines, minionsLog
import minionsRooms, minionsDB, minionsUtils

# default Python library imports
import sys
from time import strftime, localtime


class Users(StatefulTelnetProtocol):
    # User stats
    playerid           = None
    name               = ""
    lastname           = ""
    password           = ""
    level              = 0
    strength           = 0
    agility            = 0
    intelligence       = 0
    wisdom             = 0
    charm              = 0
    health             = 0
    hp                 = 50
    maxhp              = 100
    mana               = 25
    maxmana            = 50
    mr                 = 0
    stealth            = 0
    weight             = 0
    room               = 1
    resting            = False
    vision             = 1
    spellcasting       = 0
    blind              = False
    briefDesc          = 0
    moving             = 0
    holding            = {}
    wearing            = { 'arms':         None,
                           'head':         None,
                           'torso':        None,
                           'l_finger':     None,
                           'r_finger':     None,
                           'legs':         None,
                           'neck':         None,
                           'feet':         None,
                         }

    def connectionMade(self):
        # Limit how many can connect at one time
        print self.transport.getPeer().host + " CONNECTED!"
        #print "Connected"
        if len(self.factory.players) > 10:
            self.transport.write("Too many connections, try later")
            self.disconnectClient()
        self.STATUS = minionDefines.LOGIN
        minionsParser.LoginPlayer(self, "")


    def disconnectClient(self):
        global RoomList
        self.sendLine("Goodbye")
        if self.factory.players.has_key(self.playerid):
           del minionsRooms.RoomList[self.room].Players[self.playerid]
           del self.factory.players[self.playerid]
           self.factory.sendMessageToAllClients(minionDefines.BLUE + self.name + " just logged off.")
           print strftime("%b %d %Y %H:%M:%S ", localtime()) + self.name + " just logged off."
        self.transport.loseConnection()

    def connectionLost(self, reason):
        global RoomList
        # If player hungup, disconnectClient() didn't remove the user, remove them now
        if self.factory.players.has_key(self.playerid):
            del minionsRooms.RoomList[self.room].Players[self.playerid]
            del self.factory.players[self.playerid]
            self.factory.sendMessageToAllClients(minionDefines.BLUE + self.name + " just hung up!")
            print strftime("%b %d %Y %H:%M:%S ", localtime()) + self.name + " just hung up!"

    def lineReceived(self, line):
        minionsParser.commandParser(self, line)
        #self.say(line)

    #def keystrokeReceived(
    def say(self, line):
        self.sendToPlayer("You say, " + line + minionsDefines.WHITE)

    def sendToPlayer(self, line):
        self.sendLine(line + minionDefines.WHITE)



    ################################################
    # Send to everyone in current room but player
    ################################################
    def sendToRoom(self, line):
        global RoomList
        for pid in minionsRooms.RoomList[self.room].Players.keys():
            if self.factory.players[pid] == self:
                pass
            else:
                if self.factory.players[pid].STATUS == minionDefines.PLAYING:
                    self.factory.players[pid].sendToPlayer(line + minionDefines.WHITE)

    ################################################
    # Send to everyone in current room
    ################################################
    def BroadcastToRoom(self, line):
        global RoomList
        for pid in minionsRooms.RoomList[self.room].Players.keys():
            if self.factory.players[pid].STATUS == minionDefines.PLAYING:
               self.factory.players[pid].sendToPlayer(line + minionDefines.WHITE)

    ################################################
    # Send to everyone in current room but victim and player
    ################################################
    def sendToRoomNotVictim(self, victim, line):
        global RoomList
        for pid in minionsRooms.RoomList[self.room].Players.keys():
            if self.factory.players[pid] == self:
                pass
            elif pid == victim:
                pass
            else:
                if self.factory.players[pid].STATUS == minionDefines.PLAYING:
                    self.factory.players[pid].sendToPlayer(line + minionDefines.WHITE)


    ################################################
    # Shout to everyone                            #
    ################################################
    def Shout(self, line):
        for player in self.factory.players.values():
           if player.STATUS == minionDefines.PLAYING:
               player.sendToPlayer(line + minionDefines.WHITE)








class SonzoFactory(ServerFactory):
    def __init__(self):
        #self.RoomList = {}
        self.players = {}
        minionsDB.LoadRooms(self)

    def sendMessageToAllClients(self, mesg):
        for client in self.players.values():
           if client.STATUS == minionDefines.PLAYING:
               client.sendLine(mesg + minionDefines.WHITE)

    def DoNaturalHealing(self):
       for player in self.players.values():
          if player.hp != player.maxhp or player.mana != player.maxmana:
             minionsUtils.NaturalHealing(player)


    def Shutdown(self):
        reactor.stop()
        #sys.exit()

#Create server factory
factory = SonzoFactory()
# Start listener on port 23 (telnet)
factory.protocol = lambda: TelnetTransport(Users)
reactor.listenTCP(23, factory)
# Natural healing process ever 15 seconds
Healer = LoopingCall(factory.DoNaturalHealing)
Healer.start(15)
reactor.run()