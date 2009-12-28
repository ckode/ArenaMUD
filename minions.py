from twisted.internet.protocol import ServerFactory
from twisted.internet import defer
# Twisted specific imports
from twisted.python import failure, util
from twisted.internet import reactor
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol

# Minions specific imports
import minionsParser, minionsPlayer, minionDefines
import minionsParser, minionsPlayer, minionDefines, minionsLog
import minionsRooms, minionsDB

# default Python library imports
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
                           'feet':         None,
                         }

    delimiter_list = { 1: '\n', 2: '\r\n', 3: '\r\000', 4: '\r\0' }
#    delimiter = "\r\n"
#    __buffer = ""

    def connectionMade(self):


        # Limit how many can connect at one time
        #print str(self.transport.host) + " CONNECTED!"
        print "Connected"
        self.enableLocal(chr(1))
        if len(self.factory.players) > 10:
            self.transport.write("Too many connections, try later")
            self.disconnectClient()
        self.STATUS = minionDefines.LOGIN
        minionsParser.LoginPlayer(self, "")


#"""
#    def dataReceived(self, data):
#        delimiter = """
#        """Protocol.dataReceived.
#        Translates bytes into lines, and calls lineReceived (or
#        rawDataReceived, depending on mode.)
#        """
#        print str(len(data)) + " " + repr(data)
#        data1 = ""
#        print data
#        for each in data:
#           print str(len(each)) + " " + each
#           if each == '\000':
#               print "Found 000"
#          #     data1 = '\n\r'
#           elif each == chr(0):
#               print "Found r null"
#         #      data1 = '\n\r'
#           elif each == chr(0):
#               print "Found null"
#               pass
#           elif each == chr(13):
#               print "Found just r"
#               data1 = data1 + '\r\n'
#           elif each == chr(10):
#               print "Found just n"
#               data1 = data1 + '\r\n'
#           else:
##        data = data1

#        for each in data:
#           print repr(each)
#        self.__buffer = self.__buffer+data
#        for key, value in self.delimiter_list.items():
#           if value in data:
#              print key
#              delimiter = value
#
#
#        while self.line_mode and not self.paused:
#"""            try:
#                print "DELIMITER: " + repr(delimiter)
#                line, self.__buffer = self.__buffer.split(delimiter, 1)
#                print "LINE: " + line + " BUFFER: " + self.__buffer
#                delimiter = ""
#            except ValueError:
#                if len(self.__buffer) > self.MAX_LENGTH:
#                    line, self.__buffer = self.__buffer, ''
#                    return self.lineLengthExceeded(line)
#                break
#            else:
#                #print "LINE: " + repr(line)
#                linelength = len(line)
#                if linelength > self.MAX_LENGTH:
#                    exceeded = line + self.__buffer
#                    self.__buffer = ''
#                    return self.lineLengthExceeded(exceeded)
#                why = self.lineReceived(line)
#                if why or self.transport and self.transport.disconnecting:
#                    return why     """


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
            self.factory.sendMessageToAllClients(minionDefines.BLUE + self.name + " just hung up!")
            print strftime("%b %d %Y %H:%M:%S ", localtime()) + self.name + " just hung up!"

    def lineReceived(self, line):
        minionsParser.commandParser(self, line)
        #self.say(line)

    #def keystrokeReceived(
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
#factory.protocol = lambda: TelnetTransport(Users)
reactor.listenTCP(23, factory)
reactor.run()