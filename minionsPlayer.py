from twisted.internet import defer
from twisted.python import failure, util
import minionDefines



#class player():

    # Create player instance
#    ___init___():
#       name = ""

def createPlayer(user):
    user.STATUS = minionDefines.GETNAME
    user.transport.write("Enter your username: ")
    
    
