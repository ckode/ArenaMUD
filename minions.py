from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ServerFactory
from twisted.internet import defer
from twisted.python import failure, util
from twisted.internet import reactor
import minionsParser, minionsPlayer, minionDefines





class Users(LineReceiver):
    name = ""

    def connectionMade(self):
        
        self.factory.players.append(self)
        # Limit how many can connect at one time
        if len(self.factory.players) > 10:
            self.transport.write("Too many connections, try later")
            self.disconnectClient()
        self.transport.write("Current Connections: " + str(len(self.factory.players)) + "\n\r")
        minionsPlayer.createPlayer(self)



    def disconnectClient(self):
        self.sendLine("Goodbye")
        self.factory.players.remove(self)
        self.factory.sendMessageToAllClients(self.name + " has quit.")
        self.transport.loseConnection()

    def lineReceived(self, line):
        minionsParser.commandParser(self, line)
        #self.say(line)


    def say(self, line):
        self.sendToPlayer("You say, " + line)

    def sendToPlayer(self, line):
        self.sendLine(line)

    # Send to everyone in room
    def sendToRoom(self, line):
        for player in self.factory.players:
            if player == self:
                self.say(line)
            else:
                player.sendToPlayer(self.name + " says, " + line)

class SonzoFactory(ServerFactory):
    protocol = Users

    def __init__(self):
        self.players = []
 
    def sendMessageToAllClients(self, mesg): 
        for client in self.players:
            client.sendLine(mesg)



#Create server factory
factory = SonzoFactory()
# Start listener on port 23 (telnet)
reactor.listenTCP(23, factory)
reactor.run()