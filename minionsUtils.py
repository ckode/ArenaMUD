from twisted.internet import reactor

import minionsRooms, minionDefines

import re

MessageList = {}

#################################################
# WhoIsInThheRoom()
#
# Returns a dictionary of PlayerIDs mapped to
# Player's name from Room->Players dictionary
# of what players are in that room
#################################################
def WhoIsInTheRoom(player, RoomID):
   global RoomList

   PlayerList = {}

   _players = minionsRooms.RoomList[RoomID].Players.keys()
   for each in _players:
       PlayerList[each] = player.factory.players[each].name

   return PlayerList

#################################################
# FindPlayerInRoom()
#
# Finds a player in a room to preform an action
# or attack on.
#################################################
def FindPlayerInRoom(player, Name):
   global RoomList
   victimList = {}

   NameSearch = re.compile( re.escape(Name.lower()) )
   for pid, pname in minionsRooms.RoomList[player.room].Players.items():
      if pname != "":
         if NameSearch.match( pname.lower() ):
            victimList[pid] = pname

   return victimList

 #  if len(victimList) == 0:
 #     player.sendToPlayer("You do not see " + Name + " here!")
 #     return victimList
 #  elif len(victimList) == 1:
 #     return victimList
 #  else:
 #     player.sendToPlayer("Who did you mean: ")
 #     for victim in victimList.values():
 #        player.sendToPlayer(" - " + victim)
 #     return {}

#################################################
# StatLine()
#
# Sends the players statline (health and mana)
#################################################
def StatLine(player):
   # Send a players stat line
   STATLINE = "[HP=%d/%d MANA=%d/%d]: " % (player.hp, player.maxhp, player.mana, player.maxmana)
   STATSIZE = len(STATLINE)
   player.transport.write(minionDefines.SAVECUR)
   player.transport.write(minionDefines.FIRSTCOL)
   player.transport.write(chr(27) + "[" + str(STATSIZE) + ";C")
   player.transport.write(minionDefines.DELETELEFT)
   player.transport.write(minionDefines.FIRSTCOL)
   player.transport.write(STATLINE + minionDefines.RESTORECUR)


#################################################
# NaturalHealing()
#
# This is excuted as the normal healing of a
# player.  Healing rate is doubled if resting
#################################################
def NaturalHealing(player):
   healRate = 4
   manaRate = 2
   if player.resting:
      healRate = healRate * 2
      manaRate = manaRate * 2
   if (player.hp + healRate) > player.maxhp:
      player.hp = player.maxhp
   else:
      player.hp += healRate
   if (player.mana + manaRate) > player.maxmana:
      player.mana = player.maxmana
   else:
      player.mana += manaRate
   StatLine(player)

##################################################
# DisplayAction()
#
# Displays action when secret door is opened
##################################################
def DisplayAction(player, ActionID):
    global RoomList
    global RoomActionID

    ActionList = minionsRooms.RoomActionID[ActionID].split("|")
    player.sendToPlayer(minionDefines.BLUE + ActionList[0] % ("You",) )
    player.sendToRoom(minionDefines.BLUE + ActionList[0] % (player.name,) )
    player.BroadcastToRoom(minionDefines.BLUE + ActionList[1])

