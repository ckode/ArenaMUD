from twisted.internet import reactor

import minionsRooms, minionDefines, minionsCommands

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
   STATLINE = "[HP=%d/%d]: " % (player.hp, player.maxhp)
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

###################################################
# PlayerTimeBasedSpells()
#
# *** Add code to make this work, dummy function for now ***
#
# Applies over time based spell effects (like DoT and healing spells)
###################################################
def PlayerTimeBasedSpells(player):
    return

###################################################
# RoomTimeBasedSpells()
#
# *** Add code to make this work, dummy function ***
#
# Applies and over time spells that are attach to a room
# (ie, lava, fumse, fire / heat in the room.)
###################################################
def RoomTimeBasedSpells(factory, roomid):
    global players

    spell = 1
    room = minionsRooms.RoomList[roomid]
    if room.RoomNum == 2:
        for _playerid in room.Players.keys():
            _player = factory.players[_playerid]

            ApplySpellEffects(_player, spell)

###################################################
# ApplySpellEffects()
#
# ** Apply Spells effects to player
###################################################
def ApplySpellEffects(player, spell):

    player.sendToPlayer("You feel sick.")
    player.hp = player.hp - 4
    if player.hp < 1:
        KillPlayer(player)

###################################################
# KillPlayer()
#
# Kill the fool, and tell him to stay off my lines!
###################################################
def KillPlayer(player):
    player.hp = player.maxhp
    player.sendToPlayer("You are dead.")
    player.sendToRoom("%s collapses in a heap and dies." % (player.name))
    del minionsRooms.RoomList[player.room].Players[player.playerid]
    minionsRooms.RoomList[1].Players[player.playerid] = player.name
    player.room = 1
    minionsCommands.Look(player, player.room)
    player.sendToRoom("%s%s appears in a flash!%s" % (minionDefines.YELLOW, player.name, minionDefines.WHITE) )





