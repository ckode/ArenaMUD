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

import copy, random

from twisted.internet import reactor

import amDefines, amUtils, amCombat, amLog

ItemsList       = {}
SpellList       = {}

HP              = 1
MAXHP           = 2
OFFENSE         = 3
DEFENSE         = 4
SPELLCASTING    = 5
MAGICRES        = 6
DAMAGEBONUS     = 7
STEALTH         = 8
HEALBONUS       = 9
HELD            = 10
STUN            = 11
EXTRA_MELEE_DMG = 12

# Type
ITEM            = 0
SPELL           = 1

# CastOn
SELF            = 1
VICTIM          = 2
ALL             = 3

class Spells():
    def __init__( self ):
        self.SpellID                     = 0
        self.name                        = ""
        self.cmd                         = ""
        self.stype                       = 0    # Is it an item or spell
        self.UsedOn                      = 0    # Who it can be used on, 1 self, 2 victim, 3 both
        self.CoolDown                    = 0
        self.CasterID                    = 0
        self.Class                       = 0    # Required class to cast
        self.duration                    = 0    # Duration count. (1 subtracted each duration)
        self.durationEffect              = False
        self.effects                     = {}   # Dict of the effects  "STAT: Value"
        self.gesture                     = {}
        self.effectText                  = ""
        self.spellTextSelf               = ""
        self.spellTextRoom               = ""
        self.spellTextVictim             = ""
        self.WearOffText                 = ""
        self.failText                    = ""
        self.statusText                  = ""



    ###################################################################
    # ApplySpell
    #
    # The spell has been casted (item picked up)  Apply it's effect
    # On the player
    ###################################################################

    def ApplySpell(self, player, caster):
    
        # Caster has to cool down after casting
        SpellSeed = random.randint(1, 10000)
        caster.SpellsCasted[self.SpellID] = SpellSeed
        # Add CallLater to reset the spell so player can cast it again
        reactor.callLater(self.CoolDown, amUtils.ResetSpellCooldown, caster, self.SpellID, SpellSeed)
        
        # Does he make a guesture or pick it up?  If so, tell everyone
        if self.gesture != "*":
            curGesture = self.gesture.split("|")
            caster.sendToPlayer( curGesture[0] % (amDefines.BLUE, amDefines.WHITE) )
            caster.sendToRoom( curGesture[1] % (amDefines.BLUE, caster.name, amDefines.WHITE) )

        # Tell everyone
        if caster.playerid == player.playerid:
            victim = "yourself"
            if self.spellTextSelf != "*":
                caster.sendToPlayer( self.spellTextSelf % (amDefines.BLUE, victim, amDefines.WHITE) )
            if self.spellTextRoom != "*":
                caster.sendToRoom( self.spellTextRoom % (amDefines.BLUE, caster.name, player.name, amDefines.WHITE) )
        else:
            if self.spellTextSelf != "*":
                caster.sendToPlayer( self.spellTextSelf % (amDefines.BLUE, player.name, amDefines.WHITE))
            if self.spellTextRoom != "*":
                player.sendToPlayer( self.spellTextVictim % (amDefines.BLUE, caster.name, amDefines.WHITE) )
            if self.spellTextRoom != "*":
                caster.sendToRoomNotVictim( player.playerid, self.spellTextRoom % (amDefines.BLUE, caster.name, player.name, amDefines.WHITE) )
            
        # If it is a duration effect spell, apply the effects.
        if self.duration:
            # Apply any stat changes
            self.ApplySpellStats(player)
            
            # Make a Deep copy of the spell, so we can edit its attributes (casterid, subtract duration, etc) without messing up the original
            player.Spells[self.cmd] = amUtils.CopySpell(self)


            player.Spells[self.cmd].CasterID = caster.playerid
            player.Spells[self.cmd].duration -= 1
            player.Spells[self.cmd].ApplyImmediateEffects( player, caster )
        else:
            self.ApplySpellStats(player)
            self.ApplyImmediateEffects(player, caster)
            
        amUtils.StatLine(player)
    

    #===============================================
    # ApplyItem()
    #
    # Apply whatever item was picked up
    #===============================================
    def ApplyItem(self, player):
          
        if self.gesture != "*":
            curGesture = self.gesture.split("|")
            player.sendToPlayer( curGesture[0] % (amDefines.BLUE, amDefines.WHITE) )
            player.sendToRoom( curGesture[1] % (amDefines.BLUE, player.name, amDefines.WHITE) )
            
        # If it is a duration effect spell, apply the effects.
        if self.duration:
            # Apply any stat changes
            self.ApplySpellStats(player)
            
            # Make a Deep copy of the spell, so we can edit its attributes (casterid, subtract duration, etc) without messing up the original
            player.Spells[self.SpellID] = amUtils.CopySpell(self)


            player.Spells[self.SpellID].CasterID = player.playerid
            player.Spells[self.SpellID].duration -= 1
            player.Spells[self.SpellID].ApplyImmediateEffects( player, player )
        else:
            self.ApplySpellStats(player)
            self.ApplyImmediateEffects(player, player)
            
        amUtils.StatLine(player)
        
    ############################################################
    # DurationSpellEffects()
    #
    # Apple effect of duration spell
    ############################################################
    def DurationSpellEffects(self, player):

        # is the duration effect over? if so, get rid of it, or subtract one from duration
        if self.duration == 0:
            self.RemoveSpell(player)
            return
        else:
            self.duration -= 1

        # If the spell is an EoT spell, apply the effects
        if self.durationEffect:
            for (stat, value) in self.effects.items():
                if "%" in value:
                    try:
                        stat = int(stat)
                        minval, maxval = value.split("%")
                        value = random.randint( int(minval), int(maxval) )
                    except:
                        amLog.Logit("Error applying duration effect spliting effect values")
                        return
                else:
                    try:
                        stat = int(stat)
                        value = int(value)
                    except:
                        amLog.Logit( "Error converting stats/values in DurationSpellEffects()" )
                            
                # Apply the effects
                if stat == HP:
                    if (player.hp + value) > player.maxhp:
                        player.hp = player.maxhp
                    else:
                        player.hp += value
                    
                # Tell player about effects if exist
                if self.effectText != "*":
                    player.sendToPlayer( self.effectText % (amDefines.BLUE, amDefines.WHITE) )
            
        amUtils.StatLine( player )
        if player.hp < 1:
            amCombat.KillPlayer(player, self.CasterID)

    #=============================================================
    # ApplyImmediateEffects()
    #
    #=============================================================
    def ApplyImmediateEffects(self, player, caster):
        # If the spell is an EoT spell, apple the effects
        for (stat, value) in self.effects.items():
            if "%" in value:
                try:
                    stat = int(stat)
                    minval, maxval = value.split("%")
                    value = random.randint( int(minval), int(maxval) )
                except:
                    amLog.Logit("Error applying duration effect spliting effect values")
                    return
            else:
                try:
                    stat = int(stat)
                    value = int(value)
                except:
                    amLog.Logit( "Error converting stats/values in DurationSpellEffects()" )
                
            # Apply stats        
            if stat == HP:
                if (player.hp + value) > player.maxhp:
                    player.hp = player.maxhp
                else:
                    player.hp += value
        amUtils.StatLine( player )
        if player.hp < 1:
            amCombat.KillPlayer( player, caster.playerid )


    ##############################################################
    # ApplySpellStats()
    #
    # Apply stats
    ##############################################################
    def ApplySpellStats(self, player):
       # Apply Stat changes
        for stat, val in self.effects.items():
            stat = int(stat)
            
            # Ensure val isn't a range (ie, include a % that can't be converted to an INT)
            if "%" not in val:
                val = int(val)
            
            if stat == MAXHP:
                player.maxhp += val
            elif stat == DEFENSE:
                player.defense += val
            elif stat == OFFENSE:
                player.offense += val
            elif stat == SPELLCASTING:
                player.spellcasting += val
            elif stat == MAGICRES:
                player.magicres += val
            elif stat == DAMAGEBONUS:
                player.damagebonus += val
            elif stat == STEALTH:
                player.stealth += val
            elif stat == HEALBONUS:
                player.HealBonus += val
            elif stat == HELD:
                player.held = True   
            elif stat == STUN:
                player.stun            = True
                player.resting         = False
                player.attacking       = 0
                player.factory.CombatQueue.RemoveAttack(player.playerid)
            elif stat == EXTRA_MELEE_DMG:
                player.extraDamageSpell[self.SpellID] = self.effectText
               

    ##############################################################
    # RemoveSpellStats()
    #
    # Remove the spell and tell the player it wore off
    ##############################################################
    def RemoveSpell(self, player):
       # Remove Spell effects (leave HP alone)
        for stat, val in self.effects.items():
            stat = int(stat)
            
            # Ensure val isn't a range (ie, include a % that can't be converted to an INT)
            if "%" not in val:
                val = int(val)
                    
            if stat == MAXHP:
                player.maxhp -= val
            elif stat == DEFENSE:
                player.defense -= val
            elif stat == OFFENSE:
                player.offense -= val
            elif stat == SPELLCASTING:
                player.spellcasting -= val
            elif stat == MAGICRES:
                player.magicres -= val
            elif stat == DAMAGEBONUS:
                player.damagebonus -= val
            elif stat == STEALTH:
                player.stealth -= val
            elif stat == HEALBONUS:
                player.HealBonus -= val
            elif stat == HELD:
                player.held = False
            elif stat == STUN:
                player.stun              = False
            elif stat == EXTRA_MELEE_DMG:
                player.extraDamageSpell.clear()
                

        player.sendToPlayer( self.WearOffText % (amDefines.BLUE, amDefines.WHITE) )
        
        # If effect of type spell, remove it
        if self.stype == SPELL:
            del player.Spells[self.cmd]
        # if of type item, remove it.
        elif self.stype == ITEM:
            del player.Spells[self.SpellID]
