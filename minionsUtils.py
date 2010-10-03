from twisted.internet import reactor

import minionsRooms, minionDefines, minionsCommands, minionsUtils

import re, random

MessageList   = {}

class CombatQueue():
    def __init__(self):
        self.QueueIndex = {}
        self.combatQueue = []

    # Add new combat attack to CombatList
    def AddAttack(self, playerid):
        # Is the player already attacking? If so, delete old attack and add new one
        if playerid in self.QueueIndex.keys():
            del self.combatQueue[self.QueueIndex[playerid]]
            self.combatQueue.append(playerid)
            self.UpdateIndex()
        # Not already attacking, so just add combat to queue
        else:
            self.combatQueue.append(playerid)
            self.QueueIndex[playerid] = (len(self.combatQueue) - 1)


    # Remove players combat from CombatQueue
    def RemoveAttack(self, playerid):
        if playerid in self.QueueIndex.keys():
            del self.combatQueue[self.QueueIndex[playerid]]
            self.UpdateIndex()

    # Reindex QueueIndex after combatQueue Deletion
    def UpdateIndex(self):

        self.QueueIndex.clear()
        for playerid in self.combatQueue:
            x = 0
            self.QueueIndex[playerid] = x
            x += 1

    # Get combat queue for processing
    def GetCombatQueue(self):
        return self.combatQueue[:]

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
#   player.transport.write(chr(27) + "[" + str(STATSIZE) + ";C")
#   player.transport.write(minionDefines.DELETELEFT)
#   player.transport.write(minionDefines.FIRSTCOL)
   player.transport.write(STATLINE)
   player.transport.write(minionDefines.RESTORECUR)


#################################################
# NaturalHealing()
#
# This is excuted as the normal healing of a
# player.  Healing rate is doubled if resting
#################################################
def NaturalHealing(player):
   healRate = 4
   if player.resting:
      healRate = healRate * 2
   if (player.hp + healRate) > player.maxhp:
      player.hp = player.maxhp
   else:
      player.hp += healRate
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
    if room.RoomSpell != 0:
        for _playerid in room.Players.keys():
            _player = factory.players[_playerid]

            ApplySpellEffects(_player, room.RoomSpell)

###################################################
# ApplySpellEffects()
#
# ** Apply Spells effects to player
###################################################
def ApplySpellEffects(player, spell):

    spell = minionsRooms.RoomSpellList[spell]

    if spell.hp_adjust > 0:
        _textcolor = minionDefines.BLUE
    else:
        _textcolor = minionDefines.RED
    hpValue = player.hp + spell.hp_adjust
    if hpValue > player.maxhp:
        player.hp = player.maxhp
        player.sendToPlayer("%s%s%s" % (_textcolor, spell.desc, minionDefines.WHITE) )
    elif hpValue < 1:
        player.sendToPlayer("%s%s%s" % (_textcolor, spell.desc, minionDefines.WHITE) )

        KillPlayer(player, 0)
        return
    else:
        player.hp = hpValue
    player.sendToPlayer("%s%s%s" % (_textcolor, spell.desc, minionDefines.WHITE) )

###################################################
# SpringTrap()
#
# Springs any traps in the room
###################################################
def SpringRoomTrap(player, trap):
    # Sub Function to do specific stuff for room description
    def SendRoomDesc(player, desc):
        # Is players name used by embeding a %s? if so send it this one
        if "%s" in desc:
            player.sendToRoom(desc % (player.name))
        # else, send just the string
        else:
            player.sendToRoom(desc)


    trap = minionsRooms.RoomTrapList[trap]
    if trap.value > 0:
        _textcolor = minionDefines.BLUE
    else:
        _textcolor = minionDefines.RED

    # If this is an HP stat change, do HP death/maxhp checks
    if trap.stat == 1: # 1 = HP
        hpValue = player.hp + trap.value
        if hpValue > player.maxhp:
            player.hp = player.maxhp
            player.sendToPlayer("%s%s%s" % (_textcolor, trap.playerdesc, minionDefines.WHITE) )
        elif hpValue < 1:
            player.sendToPlayer("%s%s%s" % (_textcolor, trap.playerdesc, minionDefines.WHITE) )
            SendRoomDesc(player, trap.roomdesc)
            KillPlayer(player, 0)
            return
        else:
            player.hp = hpValue
            player.sendToPlayer("%s%s%s" % (_textcolor, trap.playerdesc, minionDefines.WHITE) )
            SendRoomDesc(player, trap.roomdesc)


###################################################
# KillPlayer()
#
# Kill the fool, and tell him to stay off my lines!
###################################################
def KillPlayer(player, killer):
    global CombatQueue

    player.deaths               += 1
    player.hp                    = player.maxhp
    curRoom                      = player.room


    player.attacking             = 0
    player.victim                = 0

    # Remove any combat in combat queue
    player.factory.CombatQueue.RemoveAttack(player.playerid)
    del minionsRooms.RoomList[player.room].Players[player.playerid]
    player.sendToPlayer("You are dead.")
    player.sendToRoom("%s collapses in a heap and dies." % (player.name))
    player.sendToPlayer("%s*Combat Off*%s" % (minionDefines.RED, minionDefines.WHITE) )

    # Was he killed by someone? Tell everyone.
    if killer > 0:
        killer = player.factory.players[killer]
        player.factory.sendMessageToAllClients("\r\n%s%s has killed %s!" % (minionDefines.BLUE, killer.name, player.name))
    else:
        player.factory.sendMessageToAllClients("\r\n%s%s was killed!%s" % (minionDefines.BLUE, player.name, minionDefines.WHITE))


    for _player in minionsRooms.RoomList[curRoom].Players.keys():
        otherplayer = player.factory.players[_player]
        if otherplayer.victim == player.playerid:
           otherplayer.attacking    = 0
           otherplayer.victim       = 0
           otherplayer.factory.CombatQueue.RemoveAttack(otherplayer.playerid)
           otherplayer.sendToPlayer("%s*Combat Off*%s" % (minionDefines.RED, minionDefines.WHITE) )

    minionsRooms.RoomList[1].Players[player.playerid] = player.name
    player.room = 1
    minionsCommands.Look(player, player.room)
    player.sendToRoom("%s%s appears in a flash!%s" % (minionDefines.YELLOW, player.name, minionDefines.WHITE) )


###################################################
# PlayerAttack()
#
# Attack the player if he is in the room
###################################################
def PlayerAttack(player):
    global CombatQueue

    if player.attacking == 0:
        return

    # Is the victim in the room?  If so, do attack
    if player.victim in minionsRooms.RoomList[player.room].Players.keys():
        # Shorten var path to curVictim
        curVictim = player.factory.players[player.victim]

        # Get the class/weapon attack messages for swings and misses
        Message = minionsUtils.MessageList[player.weapontext].split("|")

        # Roll damage and tell the room
        damage = random.randint(player.mindamage, player.maxdamage)
        player.sendToPlayer(Message[1] % (minionDefines.RED, curVictim.name, damage, minionDefines.WHITE) )
        curVictim.sendToPlayer(Message[3] % (minionDefines.RED, player.name, damage, minionDefines.WHITE) )
        player.sendToRoomNotVictim(curVictim.playerid, Message[5] % (minionDefines.RED, player.name, curVictim.name, damage, minionDefines.WHITE))

        # Apply the damage roll, the check to see if player is dead.
        curVictim.hp -= damage
        StatLine(curVictim)
        if curVictim.hp < 1:
            player.attacking = 0
            player.victim = 0
            player.factory.CombatQueue.RemoveAttack(player.playerid)
            KillPlayer(curVictim, player.playerid)
            player.kills += 1
            player.sendToPlayer("%s*Combat Off*%s" % (minionDefines.RED, minionDefines.WHITE) )
    else:
        player.attacking = 0
        player.victim = ""
        # Remove any combat in combat queue
        player.factory.CombatQueue.RemoveAttack(player.playerid)
        player.sendToPlayer("%s*Combat Off*%s" % (minionDefines.RED, minionDefines.WHITE) )
        return


