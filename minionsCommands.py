import minionDefines



################################################
# Command -> QUIT
################################################
def Quit(player):
   player.disconnectClient()
   
################################################
# Command -> Gossip
################################################
def Gossip(player, line):
    #cmdLen = len(cmd[0]) + 1
    #player.Shout(minionDefines.MAGENTA + player.name + " gossips: " + line[cmdLen:] + minionDefines.WHITE )
    player.Shout(minionDefines.MAGENTA + player.name + " gossips: " + line)

################################################
# Command -> Who
################################################
def Who(player):
    player.sendToPlayer(minionDefines.CYAN + "<<=-=-=-=-= Whos Online =-=-=-=>>")
    for user in player.factory.players:
        player.sendToPlayer(minionDefines.CYAN + "  => " + minionDefines.MAGENTA + user.name)
    player.sendToPlayer(minionDefines.CYAN + "<<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>>")
    
################################################
# Command -> Say
################################################
def Say(player, line):
    player.sendToRoom(minionDefines.GREEN + player.name + " says: " + minionDefines.WHITE + line)
    player.sendLine(minionDefines.GREEN + "You say: " + minionDefines.WHITE + line + minionDefines.WHITE)
    
################################################
# Command -> Emote
################################################
def Emote(player, line):
    player.sendToRoom(minionDefines.BLUE + player.name + " " + line)
    player.sendLine(minionDefines.BLUE + player.name + " " + line + minionDefines.WHITE)
