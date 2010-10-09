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
    race               = 0
    Class              = 0
    health             = 0
    isAdmin            = 0
    hp                 = 50
    maxhp              = 100
    ac                 = 0
    stealth            = 0
    ClassStealth       = False
    sneaking           = False
    room               = 1
    resting            = False
    kills              = 0
    deaths             = 0
    attackroll         = 0
    attacking          = 0
    victim             = 0
    vision             = 1
    spellcasting       = 0
    weapontext         = 0
    mindamage          = 0
    maxdamage          = 0
    blind              = False
    magery             = 0
    briefDesc          = 1
    moving             = 0

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
           if self.STATUS == minionDefines.PLAYING:
               del minionsRooms.RoomList[self.room].Players[self.playerid]
           del self.factory.players[self.playerid]
           self.factory.sendMessageToAllClients(minionDefines.BLUE + self.name + " just logged off.")
           print strftime("%b %d %Y %H:%M:%S ", localtime()) + self.name + " just logged off."
        self.transport.loseConnection()

    def connectionLost(self, reason):
        global RoomList
        # If player hungup, disconnectClient() didn't remove the user, remove them now
        if self.factory.players.has_key(self.playerid):
            if self.STATUS == minionDefines.PLAYING:
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
        self.transport.write(minionDefines.DELETELEFT)
        self.transport.write(minionDefines.FIRSTCOL)
        self.sendLine(line + minionDefines.WHITE)
        if self.STATUS == minionDefines.PLAYING or self.STATUS == minionDefines.PURGATORY:
            minionsUtils.StatLine(self)

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
                    self.transport.write(minionDefines.DELETELEFT)
                    self.transport.write(minionDefines.FIRSTCOL)
                    self.factory.players[pid].sendToPlayer(line + minionDefines.WHITE)
                    minionsUtils.StatLine(self)

    ################################################
    # Send to everyone in current room
    ################################################
    def BroadcastToRoom(self, line, RoomNumber):
        global RoomList
        for pid in minionsRooms.RoomList[RoomNumber].Players.keys():
           if self.factory.players[pid].STATUS == minionDefines.PLAYING:
               self.transport.write(minionDefines.DELETELEFT)
               self.transport.write(minionDefines.FIRSTCOL)
               self.factory.players[pid].sendToPlayer(line + minionDefines.WHITE)
               minionsUtils.StatLine(self)

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
                    self.transport.write(minionDefines.DELETELEFT)
                    self.factory.players[pid].sendToPlayer(line + minionDefines.WHITE)
                    minionsUtils.StatLine(self)



    ################################################
    # Shout to everyone                            #
    ################################################
    def Shout(self, line):
        for player in self.factory.players.values():
           if player.STATUS == minionDefines.PLAYING or player.STATUS == minionDefines.PURGATORY:
               player.sendToPlayer(line + minionDefines.WHITE)








class SonzoFactory(ServerFactory):
    def __init__(self):

        self.players = {}
        self.CombatQueue = minionsUtils.CombatQueue()

        # Load map details for the database
        minionsDB.LoadDoors(self)
        minionsDB.LoadRooms(self)
        minionsDB.LoadRoomTraps(self)
        minionsDB.LoadRoomSpells(self)
        minionsDB.LoadMessages(self)
        minionsDB.LoadClasses(self)
        minionsDB.LoadRaces(self)
        minionsDB.LoadAnsiScreens()


    def sendMessageToAllClients(self, mesg):
        for client in self.players.values():
           if client.STATUS == minionDefines.PLAYING:
               client.sendLine(mesg + minionDefines.WHITE)

    # Event loop that happens every 15 seconds
    def FifteenSecondLoop(self):
       # Actions within the Fifteen seconds loop
       # 1. Natural healing

       # Do natural healing
       for player in self.players.values():
          minionsUtils.NaturalHealing(player)


    def TwoSecondLoop(self):
        # Actions within the Two second loop
        # 1.  TimeBasedSpells (like DoT spells)
        # 2. Time based spells in the room

       # Do spell effect cased on player
       for player in self.players.values():
          minionsUtils.PlayerTimeBasedSpells(player)

       # Do Room spell effect on all players in that room
       for roomid in minionsRooms.RoomList:
           minionsUtils.RoomTimeBasedSpells(self, roomid)


    # Event loops for anything that is done ever four seconds
    def FourSecondLoop(self):
        # Actions within the four second loop
        # 1.  Combat
        # 2. Trap setting

        # Loop through combat queue and execute player attacks
        for playerid in self.CombatQueue.GetCombatQueue():
           if playerid in self.players.keys():
               minionsUtils.PlayerAttack(self.players[playerid])


    def Shutdown(self):
        reactor.stop()
        #sys.exit()

#Create server factory
factory = SonzoFactory()
# Start listener on port 23 (telnet)
factory.protocol = lambda: TelnetTransport(Users)
reactor.listenTCP(23, factory)

# 4 Second Loop
FourSecondLoop = LoopingCall(factory.FourSecondLoop)
FourSecondLoop.start(4)

# 2 Second Loop
TwoSecondLoop = LoopingCall(factory.TwoSecondLoop)
TwoSecondLoop.start(2)

# Natural healing process ever 15 seconds
FifteenSecondLoop = LoopingCall(factory.FifteenSecondLoop)
FifteenSecondLoop.start(15)
reactor.run()