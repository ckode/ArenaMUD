#  ArenaMUD - A multiplayer combat game - http://arenamud.david-c-brown.com
#  Copyright (C) 2009, 2010 - David C Brown & Mark Richardson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from twisted.internet import reactor

import amRooms, amDefines, amCommands, amUtils
import amLog

import re, random, os

MessageList   = {}

###################################################
# class CombatQueue
#
# The queue that keeps combat order in sync
###################################################
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

    _players = amRooms.RoomList[RoomID].Players.keys()
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
    for pid, pname in amRooms.RoomList[player.room].Players.items():
        if pname != "":
            if NameSearch.match( pname.lower() ):
                victimList[pid] = pname

    return victimList

 #  if len(victimList) == 0: player.sendToPlayer("You do not see " + Name + "
 #  here!") return victimList elif len(victimList) == 1: return victimList
 #  else: player.sendToPlayer("Who did you mean: ") for victim in
 #  victimList.values(): player.sendToPlayer(" - " + victim) return {}

#################################################
# StatLine()
#
# Sends the players statline (health and mana)
#################################################
def StatLine(player):
    # Send a players stat line

    # If player.hp is higher than maxhp, make it blue (only a buff can do this)
    if player.hp > player.maxhp:
        hpcolor = amDefines.BLUE
    # Is the players HP less than 25% of total hps?
    elif player.hp < ( ( float(player.maxhp) / 100) * 25 ):
        hpcolor = amDefines.LRED
    else:
        hpcolor = amDefines.WHITE

    if player.resting:
        STATLINE = "[HP=%s%d%s/%d]: (resting) " % (hpcolor, player.hp, amDefines.WHITE, player.maxhp)
    else:
        STATLINE = "[HP=%s%d%s/%d]: " % ( hpcolor, player.hp, amDefines.WHITE, player.maxhp)
    if player.STATUS == amDefines.PURGATORY:
        STATLINE = "%s>" % (amDefines.WHITE)

    STATSIZE = len(STATLINE)
    player.transport.write(amDefines.SAVECUR)
    player.transport.write(amDefines.FIRSTCOL)
    player.transport.write(STATLINE)
    player.transport.write(amDefines.RESTORECUR)


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

    ActionList = amRooms.RoomActionID[ActionID].split("|")
    player.sendToPlayer(amDefines.BLUE + ActionList[0] % ("You",) )
    player.sendToRoom(amDefines.BLUE + ActionList[0] % (player.name,) )
    player.BroadcastToRoom(amDefines.BLUE + ActionList[1])

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
    room = amRooms.RoomList[roomid]
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

    spell = amRooms.RoomSpellList[spell]

    if spell.hp_adjust > 0:
        _textcolor = amDefines.BLUE
    else:
        _textcolor = amDefines.RED
    hpValue = player.hp + spell.hp_adjust
    if hpValue > player.maxhp:
        player.hp = player.maxhp
        player.sendToPlayer("%s%s%s" % (_textcolor, spell.desc, amDefines.WHITE) )
    elif hpValue < 1:
        player.sendToPlayer("%s%s%s" % (_textcolor, spell.desc, amDefines.WHITE) )

        KillPlayer(player, 0)
        return
    else:
        player.hp = hpValue
    player.sendToPlayer("%s%s%s" % (_textcolor, spell.desc, amDefines.WHITE) )

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


    trap = amRooms.RoomTrapList[trap]
    if trap.value > 0:
        _textcolor = amDefines.BLUE
    else:
        _textcolor = amDefines.RED

    # If this is an HP stat change, do HP death/maxhp checks
    if trap.stat == 1: # 1 = HP
        hpValue = player.hp + trap.value
        if hpValue > player.maxhp:
            player.hp = player.maxhp
            player.sendToPlayer("%s%s%s" % (_textcolor, trap.playerdesc, amDefines.WHITE) )
        elif hpValue < 1:
            player.sendToPlayer("%s%s%s" % (_textcolor, trap.playerdesc, amDefines.WHITE) )
            SendRoomDesc(player, trap.roomdesc)
            KillPlayer(player, 0)
            return
        else:
            player.hp = hpValue
            player.sendToPlayer("%s%s%s" % (_textcolor, trap.playerdesc, amDefines.WHITE) )
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
    player.effectingSpell        = 0
    curRoom                      = player.room



    player.attacking             = 0
    player.victim                = 0

    # Remove any combat in combat queue
    player.factory.CombatQueue.RemoveAttack(player.playerid)
    del amRooms.RoomList[player.room].Players[player.playerid]
    player.sendToPlayer("You are dead.")
    player.sendToRoom("%s collapses in a heap and dies." % (player.name))
    if player.attacking:
        player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE) )

    # Was he killed by someone? Tell everyone.
    if killer > 0:
        killer = player.factory.players[killer]
        player.factory.sendMessageToAllClients("\r\n%s%s has killed %s!" % (amDefines.BLUE, killer.name, player.name))
    else:
        player.factory.sendMessageToAllClients("\r\n%s%s was killed!%s" % (amDefines.BLUE, player.name, amDefines.WHITE))


    for _player in amRooms.RoomList[curRoom].Players.keys():
        otherplayer = player.factory.players[_player]
        if otherplayer.victim == player.playerid:
            otherplayer.attacking    = 0
            otherplayer.victim       = 0
            otherplayer.factory.CombatQueue.RemoveAttack(otherplayer.playerid)
            otherplayer.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE) )

    # Spawn the player
    EnterPurgatory(player)



###################################################
# PlayerAttack()
#
# Attack the player if he is in the room
###################################################
def PlayerAttack(player):
    global CombatQueue

    if player.attacking == 0:
        return

    player.resting = False
    # Is the victim in the room?  If so, do attack
    if player.victim in amRooms.RoomList[player.room].Players.keys():
        # Shorten var path to curVictim
        curVictim = player.factory.players[player.victim]
        curVictim.resting = False
        curVictim.sneaking = False

        # Get the class/weapon attack messages for swings and misses
        Message = amUtils.MessageList[player.weapontext].split("|")

        # Roll damage and tell the room
        damage = random.randint(player.mindamage, player.maxdamage)

        # Is attacker backstabbing?
        if player.ClassStealth and player.sneaking:

            # Backstab modifier
            modifier = ( player.maxdamage + (player.maxdamage * ( float(player.stealth) / 100 ) ) )
            damage += modifier
            player.sendToPlayer(Message[2] % (amDefines.RED, curVictim.name, damage, amDefines.WHITE) )
            curVictim.sendToPlayer(Message[5] % (amDefines.RED, player.name, damage, amDefines.WHITE) )
            player.sendToRoomNotVictim(curVictim.playerid, Message[8] % (amDefines.RED, player.name, curVictim.name, damage, amDefines.WHITE))
        else:
            # Not backstabbing, do normak damage and no surprise message
            player.sendToPlayer(Message[1] % (amDefines.RED, curVictim.name, damage, amDefines.WHITE) )
            curVictim.sendToPlayer(Message[4] % (amDefines.RED, player.name, damage, amDefines.WHITE) )
            player.sendToRoomNotVictim(curVictim.playerid, Message[7] % (amDefines.RED, player.name, curVictim.name, damage, amDefines.WHITE))

        # No more sneaking after you've attacked.
        player.sneaking = False
        # Apply the damage roll, the check to see if player is dead.
        curVictim.hp -= damage
        StatLine(curVictim)
        if curVictim.hp < 1:
            player.attacking = 0
            player.victim = 0
            player.factory.CombatQueue.RemoveAttack(player.playerid)
            KillPlayer(curVictim, player.playerid)
            player.kills += 1
            player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE) )
    else:
        player.attacking = 0
        player.victim = ""
        # Remove any combat in combat queue
        player.factory.CombatQueue.RemoveAttack(player.playerid)
        player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE) )
        return


###################################################
# SpawnPlayer()
#
# Spawns a player in an empty room (no other players)
# Of someone is in every room, just spawn the player
###################################################
def SpawnPlayer(player):
    global RoomList
    SpawnRooms = []

    player.STATUS = amDefines.PLAYING
    player.maxhp  = player.staticmaxhp

    # Look for empty rooms that allow spawning
    for room in amRooms.RoomList.values():
        if len(room.Players) == 0 and room.NoSpawn == 0:
            SpawnRooms.append(room)

    # If no empty spawn rooms where found, just get rooms that allow spawning
    if len(SpawnRooms) == 0:
        for room in amRooms.RoomList.values():
            if room.NoSpawn == 0:
                SpawnRooms.append(room)


    newRoom = SpawnRooms[( random.randint( 1, len(SpawnRooms) ) ) - 1 ]
    player.room = newRoom.RoomNum
    amRooms.RoomList[player.room].Players[player.playerid] = player.name
    amCommands.Look(player, player.room)
    player.sendToRoom("%s%s appears in a flash!%s" % (amDefines.YELLOW, player.name, amDefines.WHITE) )
    player.Shout(amDefines.BLUE + player.name + " has spawn!")

#####################################################
# EnterPurgatory()\
#
# Where a players starts after login and where he goes
# when he dies.  You have to type spawn to enter the game
#####################################################
def EnterPurgatory(player):
    player.STATUS = amDefines.PURGATORY
    amCommands.Who(player)
    player.sendToPlayer("Type 'spawn' to spawn, type 'help' for help.")