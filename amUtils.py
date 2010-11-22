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
import amLog, amMaps, amCombat, amSpells

import re, random, os

MessageList   = {}

        
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

    _players = amMaps.Map.Rooms[RoomID].Players.keys()
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
    for pid, pname in amMaps.Map.Rooms[player.room].Players.items():
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
    if len(player.Spells) == 0:
        return

    # Loop though all the spells and apply the duration effects
    for spell in player.Spells.values():
        spell.DurationSpellEffects( player )

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
    room = amMaps.Map.Rooms[roomid]
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

    spell = amMaps.Map.RoomSpells[spell]

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

        amCombat.KillPlayer(player, 0)
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


    trap = amMaps.Map.RoomTraps[trap]
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
            amCombat.KillPlayer(player, 0)
            return
        else:
            player.hp = hpValue
            player.sendToPlayer("%s%s%s" % (_textcolor, trap.playerdesc, amDefines.WHITE) )
            SendRoomDesc(player, trap.roomdesc)
###################################################
# SpawnPlayer()
#
# Spawns a player in an empty room (no other players)
# Of someone is in every room, just spawn the player
###################################################
def SpawnPlayer(player):
    global Map
    SpawnRooms = []
    
    player.STATUS       = amDefines.PLAYING
    player.maxhp        = player.staticmaxhp
    player.hp           = player.maxhp
    player.moving       = 0

    # Look for empty rooms that allow spawning
    for room in amMaps.Map.Rooms.values():
        if len(room.Players) == 0 and room.NoSpawn == 0:
            SpawnRooms.append(room)

    # If no empty spawn rooms where found, just get rooms that allow spawning
    if len(SpawnRooms) == 0:
        for room in amMaps.Map.Rooms.values():
            if room.NoSpawn == 0:
                SpawnRooms.append(room)

    newRoom = SpawnRooms[( random.randint( 1, len(SpawnRooms) ) ) - 1 ]
    player.room = newRoom.RoomNum
    amMaps.Map.Rooms[player.room].Players[player.playerid] = player.name
    amCommands.Look(player, player.room, player.briefDesc)
    player.sendToRoom("%s%s appears in a flash!%s" % (amDefines.YELLOW, player.name, amDefines.WHITE) )
    player.Shout(amDefines.BLUE + player.name + " has spawn!")

#####################################################
# EnterPurgatory()
#
# Where a players starts after login and where he goes
# when he dies.  You have to type spawn to enter the game
#####################################################
def EnterPurgatory(player):
    player.STATUS = amDefines.PURGATORY
    amCommands.Who(player)
    player.sendToPlayer("Type 'spawn' to spawn, type 'help' for help.")
    player.stun = False
    
#####################################################
# KickAllToPurgatory()
#
# Kill all combat, empty any queues necessary and then
# set the status of each player to purgatory
#####################################################
def KickAllToPurgatory(player):
    global CombatQueue
    
    player.factory.CombatQueue.KillAllCombat()
    
    for user in player.factory.players.values():

        if user.STATUS == amDefines.PLAYING or user.STATUS == amDefines.PURGATORY:
            if user.STATUS == amDefines.PLAYING:
                del amMaps.Map.Rooms[user.room].Players[user.playerid]
                user.STATUS = amDefines.PURGATORY
                user.stun = False
            user.room = 0
            
#=====================================================
# CopySpell()
#
# Make a copy of the current spell, because Python's
# deepcopy, doesn't copy the class objects methods,
# only it's attributes. (why?!?!)
#=====================================================
def CopySpell( spell ):
    newSpell = amSpells.Spells()
    
    newSpell.SpellID                     = spell.SpellID
    newSpell.name                        = spell.name 
    newSpell.cmd                         = spell.cmd 
    newSpell.stype                       = spell.stype
    newSpell.UsedOn                      = spell.UsedOn
    newSpell.CasterID                    = spell.CasterID 
    newSpell.Class                       = spell.Class
    newSpell.duration                    = spell.duration
    newSpell.durationEffect              = spell.durationEffect
    newSpell.effects                     = spell.effects
    newSpell.gesture                     = spell.gesture
    newSpell.effectText                  = spell.effectText
    newSpell.spellTextSelf               = spell.spellTextSelf
    newSpell.spellTextRoom               = spell.spellTextRoom
    newSpell.spellTextVictim             = spell.spellTextVictim
    newSpell.WearOffText                 = spell.WearOffText
    
    return newSpell