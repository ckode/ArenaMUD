from twisted.internet import defer
from twisted.python import failure, util



#class player():

    # Create player instance
#    ___init___():
#       name = ""

def createPlayer(user):
    user.sendToPlayer("Enter a name: ")
    user.lineReceived(line)
    user.name=line
