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
        minionsPlayer.createPlayer(self)



    def disconnectClient(self):
        self.sendLine("Goodbye")
        self.factory.players.remove(self)
        self.factory.sendMessageToAllClients(minionDefines.BLUE + self.name + " has quit.")
        self.transport.loseConnection()

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







class SonzoFactory(ServerFactory):
    protocol = Users

    def __init__(self):
        self.players = []
 
    def sendMessageToAllClients(self, mesg): 
        for client in self.players:
            if client.STATUS == minionDefines.PLAYING:
                client.sendLine(mesg + minionDefines.WHITE)



#Create server factory
factory = SonzoFactory()
# Start listener on port 23 (telnet)
reactor.listenTCP(23, factory)
reactor.run()