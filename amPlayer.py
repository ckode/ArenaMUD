from twisted.internet import defer
from twisted.python import failure, util
import amDefines



#class player():

    # Create player instance
#    ___init___():
#       name = ""

def createPlayer(user):
    user.STATUS = amDefines.GETNAME
    user.transport.write("Enter your username: ")


