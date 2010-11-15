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

import random
import amMaps, amUtils, amDefines


ATTACKING               = 0
CASTING                 = 1

MISS                    = 0

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

    # Delete all combat events in the queue
    def KillAllCombat(self):
        self.QueueIndex.clear()
        del self.combatQueue[:]
        

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
    del amMaps.Map.Rooms[player.room].Players[player.playerid]
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


    for _player in amMaps.Map.Rooms[curRoom].Players.keys():
        otherplayer = player.factory.players[_player]
        if otherplayer.victim == player.playerid:
            otherplayer.attacking    = 0
            otherplayer.victim       = 0
            otherplayer.factory.CombatQueue.RemoveAttack(otherplayer.playerid)
            otherplayer.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE) )

    # Spawn the player
    amUtils.EnterPurgatory(player)

        
#========================================================
# HitRoll()
#
# Calulates if a hit ocurrs returns true or false
#========================================================
def HitRoll( player, victim , ATTACKTYPE ):
    # If this a melee attack (including melee spells), or a non-melee spell based attack
    if ATTACKTYPE == ATTACKING:
        ToHitValue = victim.defense - player.offense
    elif ATTACKTYPE == CASTING:
        ToHitValue = victim.magicres - player.spellcasting
        
    Roll = random.randint(0, 100)
    
    if Roll > ToHitValue:
        return True
    else:
        return False

###################################################
# PlayerAttack()
#
# Attack the player if he is in the room
###################################################
def PlayerAttack(player):
    global CombatQueue
    
    damage = 0
    
    if player.attacking == 0:
        return

    player.resting = False
    # Is the victim in the room?  If so, do attack
    if player.victim in amMaps.Map.Rooms[player.room].Players.keys():
        # Shorten var path to curVictim
        curVictim = player.factory.players[player.victim]
        curVictim.resting = False
        curVictim.sneaking = False

        # Get the class/weapon attack messages for swings and misses
        Message = amUtils.MessageList[player.weapontext].split("|")
        
        # Is attacker backstabbing?
        if player.ClassStealth and player.sneaking:

            # Make the hit roll
            if HitRoll( player, curVictim, ATTACKING ):
                # Roll for damage and apply backstab damage modifier 
                damage = DamageRoll( player, curVictim ) + BackstabModifier( player )

                # Tell room of outcome
                SendDamageTextToRoom( player, curVictim, damage, Message[2], Message[5], Message[8] )
            else:
                # Tell room of outcome
                SendDamageTextToRoom( player, curVictim, MISS, Message[0], Message[3], Message[6] )

        else:
                # Make each attack that the attacker has per round.
                totalDamage = 0
                for attk in range(0, player.speed):  
                    # Make the hitroll
                    if HitRoll( player, curVictim, ATTACKING ):
                        # Roll damage and tell the room
                        damage = DamageRoll( player, curVictim )
                        # Total up damage thus far
                        totalDamage += damage
                        # Tell room of outcome.
                        SendDamageTextToRoom( player, curVictim, damage, Message[1], Message[4], Message[7] )
                        # Check to see if player id dead already, if so break out of attack loop!
                        if totalDamage > curVictim.hp:
                            break
                    else:
                        # Tell room of outcome
                        SendDamageTextToRoom( player, curVictim, MISS, Message[0], Message[3], Message[6] )
                        
                damage = totalDamage
            
            
        # No more sneaking after you've attacked.
        player.sneaking = False
        # Apply the damage roll, the check to see if player is dead.
        curVictim.hp -= damage
        amUtils.StatLine(curVictim)
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
    
#==================================================
# BackstabModifer()
#
# Applies damage modifications for Backstabs
#==================================================
def BackstabModifier( player ):
    bsModifier        = random.randint(player.maxdamage, ( player.maxdamage * 2 ) ) 
    StealthModifier   = player.maxdamage * ( float(player.stealth) / 100 ) 
    
    return ( bsModifier + StealthModifier )


#==================================================
# DamageRoll()
#
# Roll damage done during the attack
#==================================================
def DamageRoll( player, victim ):
    # Later, add in victim buffs that lower lower damage
    
    damage = random.randint(player.mindamage, player.maxdamage) 
    return damage

#==================================================
# SendDamageTextToRoom()
#
# Sends the combat messages to the room (damage and misses)
#==================================================
def SendDamageTextToRoom( player, victim, damage, PlayerMessage, VictimMessage, RoomMessage ):
    if damage == MISS: 
        player.sendToPlayer(PlayerMessage % (amDefines.WHITE, victim.name, amDefines.WHITE) )
        victim.sendToPlayer(VictimMessage % (amDefines.WHITE, player.name, amDefines.WHITE) )
        player.sendToRoomNotVictim(victim.playerid, RoomMessage % (amDefines.WHITE, player.name, victim.name, amDefines.WHITE))
    else:
        player.sendToPlayer(PlayerMessage % (amDefines.RED, victim.name, damage, amDefines.WHITE) )
        victim.sendToPlayer(VictimMessage % (amDefines.RED, player.name, damage, amDefines.WHITE) )
        player.sendToRoomNotVictim(victim.playerid, RoomMessage % (amDefines.RED, player.name, victim.name, damage, amDefines.WHITE))