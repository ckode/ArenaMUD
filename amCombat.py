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
        
        
#========================================================
# HitRoll()
#
# Calulates if a hit ocurrs returns true or false
#========================================================
def HitRoll( player, victim ):
    pass

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
    if player.victim in amMaps.Map.Rooms[player.room].Players.keys():
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
            # Make each attack that the attacker has per round.
            totalDamage = 0
            for attk in range(0, player.attkcount):  
                damage = random.randint(player.mindamage, player.maxdamage)
                totalDamage += damage
                # Not backstabbing, do normak damage and no surprise message
                player.sendToPlayer(Message[1] % (amDefines.RED, curVictim.name, damage, amDefines.WHITE) )
                curVictim.sendToPlayer(Message[4] % (amDefines.RED, player.name, damage, amDefines.WHITE) )
                player.sendToRoomNotVictim(curVictim.playerid, Message[7] % (amDefines.RED, player.name, curVictim.name, damage, amDefines.WHITE))
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
            amUtils.KillPlayer(curVictim, player.playerid)
            player.kills += 1
            player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE) )
    else:
        player.attacking = 0
        player.victim = ""
        # Remove any combat in combat queue
        player.factory.CombatQueue.RemoveAttack(player.playerid)
        player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE) )
        return