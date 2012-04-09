#  ArenaMUD - A multiplayer combat game - http://arenamud.david-c-brown.com
#  Copyright (C) 2009, 2010 - David C Brown & Mark Richardson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from twisted.internet.protocol import ServerFactory
from twisted.internet import defer
# Twisted specific imports
from twisted.python import failure, util
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol

# am specific imports
import amParser, amPlayer, amDefines, amLog
import amRooms, amDB, amUtils, amMaps, amCombat
import amSpells

# default Python library imports
import sys, cProfile
from time import strftime, localtime

class Users(StatefulTelnetProtocol):
    def __init__(self):
        
        # User attributes
        
        # Base stats
        self.playerid           = None
        self.ClassType          = 0
        self.name               = ""
        self.lastname           = ""
        self.password           = ""
        self.race               = 0
        self.Class              = 0
        self.health             = 0
        self.offense            = 0
        self.defense            = 0
        self.magicres           = 0
        self.damagebonus        = 0        
        self.hp                 = 0
        self.stealth            = 0
        self.spellcasting       = 0
        self.vision             = 1
        self.speed              = 0
        self.mindamage          = 0
        self.maxdamage          = 0
        
        # Class specfic 
        self.magery             = 0   # May not need this
        
        # place holders
        self.victim             = 0
        self.room               = 1
        
        
        # Max Stats 
        self.maxhp              = 0
        self.staticmaxhp        = 0
        
        # Flags
        self.isAdmin            = 0
        self.sneaking           = False             
        self.ClassStealth       = False
        self.resting            = False
        self.held               = False
        self.stun               = False
        self.HealBonus          = 0    
        self.blind              = False
        self.moving             = 0
        self.attacking          = 0
        self.briefDesc          = 1
        self.Rerolling          = False
        self.statLine           = True
        
        
        # playing stats
        self.kills              = 0
        self.deaths             = 0
    
        
        # other player information
        self.weapontext         = 0

        

        # List of things applied to the player
        self.extraDamageSpell   = {}
        self.SpellsCasted       = {}
        self.Spells             = {}




    def connectionMade(self):
        # Limit how many can connect at one time
        print self.transport.getPeer().host + " CONNECTED!"
        #print "Connected"
        if len(self.factory.players) > 10:
            self.transport.write("Too many connections, try later")
            self.disconnectClient()
        self.STATUS = amDefines.LOGIN
        amParser.LoginPlayer(self, "")


    def disconnectClient(self):
        global RoomList
        self.sendLine("Goodbye")
        if self.factory.players.has_key(self.playerid):
            if self.STATUS == amDefines.PLAYING:
                del amMaps.Map.Rooms[self.room].Players[self.playerid]
            del self.factory.players[self.playerid]
            self.factory.sendMessageToAllClients(amDefines.BLUE + self.name + " just logged off.")
            print strftime("%b %d %Y %H:%M:%S ", localtime()) + self.name + " just logged off."
        self.transport.loseConnection()

    def connectionLost(self, reason):
        global RoomList
        # If player hungup, disconnectClient() didn't remove the user, remove them now
        if self.factory.players.has_key(self.playerid):
            if self.STATUS == amDefines.PLAYING:
                del amMaps.Map.Rooms[self.room].Players[self.playerid]
            del self.factory.players[self.playerid]
            self.factory.sendMessageToAllClients(amDefines.BLUE + self.name + " just hung up!")
            print strftime("%b %d %Y %H:%M:%S ", localtime()) + self.name + " just hung up!"

    def lineReceived(self, line):
        amParser.commandParser(self, line)
        #self.say(line)

    def say(self, line):
        self.sendToPlayer("You say, " + line + amDefines.WHITE)

    def sendToPlayer(self, line):
        self.transport.write(amDefines.DELETELEFT)
        self.transport.write(amDefines.FIRSTCOL)
        self.sendLine(line + amDefines.WHITE)
        if self.STATUS == amDefines.PLAYING or self.STATUS == amDefines.PURGATORY:
            amUtils.StatLine(self)

    ################################################
    # Send to everyone in current room but player
    ################################################
    def sendToRoom(self, line):
        global RoomList

        for pid in amMaps.Map.Rooms[self.room].Players.keys():
            if self.factory.players[pid] == self:
                pass
            else:
                if self.factory.players[pid].STATUS == amDefines.PLAYING:
                    self.transport.write(amDefines.DELETELEFT)
                    self.transport.write(amDefines.FIRSTCOL)
                    self.factory.players[pid].sendToPlayer(line + amDefines.WHITE)
                    amUtils.StatLine(self)

    ################################################
    # Send to everyone in current room
    ################################################
    def BroadcastToRoom(self, line, RoomNumber):
        global RoomList
        for pid in amMaps.Map.Rooms[RoomNumber].Players.keys():
            if self.factory.players[pid].STATUS == amDefines.PLAYING:
                self.transport.write(amDefines.DELETELEFT)
                self.transport.write(amDefines.FIRSTCOL)
                self.factory.players[pid].sendToPlayer(line + amDefines.WHITE)
                amUtils.StatLine(self)

    ################################################
    # Send to everyone in current room but victim and player
    ################################################
    def sendToRoomNotVictim(self, victim, line):
        global RoomList
        for pid in amMaps.Map.Rooms[self.room].Players.keys():
            if self.factory.players[pid] == self:
                pass
            elif pid == victim:
                pass
            else:
                if self.factory.players[pid].STATUS == amDefines.PLAYING:
                    self.transport.write(amDefines.DELETELEFT)
                    self.factory.players[pid].sendToPlayer(line + amDefines.WHITE)
                    amUtils.StatLine(self)



    ################################################
    # Shout to everyone                            #
    ################################################
    def Shout(self, line):
        for player in self.factory.players.values():
            if player.STATUS == amDefines.PLAYING or player.STATUS == amDefines.PURGATORY:
                player.sendToPlayer(line + amDefines.WHITE)








class SonzoFactory(ServerFactory):
    def __init__(self):

        self.players = {}
        
        amSpells.SpellList, amSpells.ItemsList = amDB.LoadSpellsAndItems( self )
        self.CombatQueue = amCombat.CombatQueue()
        self.ArenaQueue = amMaps.ArenaQueue()
        
        # Load map details for the database

        amDB.LoadMessages(self)
        amDB.LoadClasses(self)
        amDB.LoadRaces(self)
        amDB.LoadAnsiScreens()
        


        # Disable the following until the new map queue is complete
        
        if self.ArenaQueue.ConfFileFail:
            self.ShutdownPreReactorStart()


    def sendMessageToAllClients(self, mesg):
        for client in self.players.values():
            if client.STATUS == amDefines.PLAYING or client.STATUS == amDefines.PURGATORY:
                client.sendLine(mesg + amDefines.WHITE)
                

    def sendMessageToAllClientsInRoom(self, mesg, room):
        for client in self.players.values():
            if client.STATUS == amDefines.PLAYING or client.STATUS == amDefines.PURGATORY:
                if client.room == room:
                    client.sendToPlayer(mesg)                    
                    
                
    # Event loop that happens every 15 seconds
    def FifteenSecondLoop(self):
       # Actions within the Fifteen seconds loop
       # 1. Natural healing

       # Do natural healing
        for player in self.players.values():
            amUtils.NaturalHealing(player)


    def TwoSecondLoop(self):
         # Actions within the Two second loop
         # 1.  TimeBasedSpells (like DoT spells)
         # 2. Time based spells in the room

        # Do spell effect cased on player
        for player in self.players.values():
            amUtils.PlayerTimeBasedSpells(player)

        # Do Room spell effect on all players in that room
        for roomid in amMaps.Map.Rooms:
            amUtils.RoomTimeBasedSpells(self, roomid)


    # Event loops for anything that is done ever four seconds
    def FourSecondLoop(self):
        # Actions within the four second loop
        # 1.  Combat
        #

        # Loop through combat queue and execute player attacks
        for playerid in self.CombatQueue.GetCombatQueue():
            if playerid in self.players.keys():
                amCombat.PlayerAttack(self.players[playerid])


    def ShutdownPreReactorStart(self):
        print "Shutting down due to startup error.  See ArenaMUD.log file for details"
        sys.exit(1)

    def Shutdown(self):
        reactor.stop()





# Wrapped it in main() so I can profile the game and see where improvements can be made.
def main():
    #Create server factory
    factory = SonzoFactory()

    # Check to make sure at least one map laoded.  If not, shutdown!
    try:
        tmp = len(amMaps.Map.Rooms)
    except:
        amLog.Logit("Error: No maps loaded! Shutting down...")
        factory.ShutdownPreReactorStart()
        sys.exit(1)


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
    
    
#cProfile.run('main()')
main()