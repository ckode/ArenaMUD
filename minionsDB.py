import sqlite3, minionsLog

################################################
# LoadPlayer()
#
# Loads player from database
################################################
def LoadPlayer(player, name):
    global DB
    try:
       conn = sqlite.connect(DB)
    except:
       minionsLog.Logit("Failed to open database!")
       
       
def GetUserID(name):
    return 0