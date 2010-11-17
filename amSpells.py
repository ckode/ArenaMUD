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

import amDefines, amUtils, amCombat

SpawnItems      = {}
SpellList       = {}

HP              = 1
MAXHP           = 2
OFFENSE         = 3
DEFENSE         = 4
SPELLCASTING    = 5
MAGICRES        = 6
DAMAGEBONUS     = 7
STEALTH         = 8
REGEN           = 9

# CastOn
SELF            = 1
VICTIM          = 2
ALL             = 3

class Spells():
    def __init__(self, SpellCasterID):
        self.id                          = 0
        self.name                        = ""
        self.cmd                         = ""
        self.UsedOn                      = 0    # Who it can be used on, 1 self, 2 victim, 3 both
        self.CasterID                    = 0
        self.Class                       = 0    # Required class to cast
        self.duration                    = 0    # Duration count. (1 subtracted each duration)
        self.durationEffect              = False
        self.effects                     = {}   # Dict of the effects  "STAT: Value"
        self.guesture                    = {}
        self.effectText                  = ""
        self.spellTextSelf               = ""
        self.spellTextRoom               = ""
        self.spellTextVictim             = ""
        self.WearOffText                 = ""



    ###################################################################
    # ApplySpell
    #
    # The spell has been casted (item picked up)  Apply it's effect
    # On the player
    ###################################################################

    def ApplySpell(self, player, caster):

        # Apply any stat changes
        self.ApplySpellStats(player)
        # If it is a duration effect spell, apply the effects.
        if self.durationEffect:
            self.CasterID = caster.playerid
            if player.Spells.has_key(self.id):
                player.Spells[self.id] = self
            self.DurationSpellEffects(player)
        else:
            self.ApplyImmediateEffects(player, caster)


        # Does he make a guesture or pick it up?  If so, tell everyone
        if self.guesture[0] != "*":
            player.sendToPlayer( self.guesture[0] % (amDefines.BLUE, amDefines.WHITE) )
            player.sendToRoom( self.guesture[1] % (amDefines.BLUE, player.name, amDefines.WHITE) )


        # Tell everyone
        if caster == player:
            victim = "yourself"
            player.sendToPlayer( self.spellTextSelf % (amDefines.BLUE, victim, amDefines.WHITE) )
            player.sendToRoom( self.spellTextRoom % (amDefines.BLUE, player.name, amDefines.WHITE) )
        else:
            caster.sendToPlayer( self.spellTextSelf % (amDefines.BLUE, player.name, amDefines.WHITE))
            player.sendToPlayer( self.spellTextVictim % (amDefines.BLUE, caster.name, amDefines.WHITE) )
            player.sendToRoom( self.spellTextRoom % (amDefines.BLUE, caster.name, player.name, amDefines.WHITE) )



    ############################################################
    # DurationSpellEffects()
    #
    # Apple effect of duration spell
    ############################################################
    def DurationSpellEffects(self, player):
        # is the duration effect over? if so, get rid of it, or subtract one from duration
        if self.duration == 0:
            RemoveSpellStats(player)
            return
        else:
            self.duration -= 1

        # Apply the stat changes for each spell
        for spell in player.Spells:
            # If the spell is an EoT spell, apply the effects
            if spell.durationEffect:
                for (stat, value) in self.effects.items():
                    if stat == HP:
                        if (player.hp + value) > player.maxhp:
                            player.hp = player.maxhp
                        else:
                            player.hp += value
                    
        # Tell player about effects if exist
        if self.effectText != "*":
            player.sendToPlayer( self.effectText % (amDefines.BLUE, amDefines.WHITE) )

    #=============================================================
    # ApplyImmediateEffects()
    #
    #=============================================================
    def ApplyImmediateEffects(self, player, caster):
        for spell in allbuffs:
            # If the spell is an EoT spell, apple the effects
            if not spell.durationEffect:
                for (stat, value) in self.effects.items():
                    if stat == HP:
                        if (player.hp + value) > player.maxhp:
                            player.hp = player.maxhp
                        else:
                            player.hp += value
        if player.hp < 1:
            amCombat.Killplayer( player, caster )


    ##############################################################
    # ApplySpellStats()
    #
    # Apply stats
    ##############################################################
    def ApplySpellStats(self, player):
       # Apply Stat changes
        for (stat, val) in self.effects.values():
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
            elif stat == REGEN:
                player.regen += val
                
               
                

    ##############################################################
    # RemoveSpellStats()
    #
    # Remove the spell and tell the player it wore off
    ##############################################################
    def RemoveSpellStats(self, player):
       # Remove Spell effects (leave HP alone)
        for (stat, val) in self.effects.values():
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
            elif stat == REGEN:
                player.regen -= val

        player.sendToPlayer( self.WearOffText % (amDefines.BLUE, amDefines.WHITE) )
        del player.Spells[self.id]