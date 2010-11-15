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

import amDefines, amUtils

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
    def __init__(self):
        self.id                          = 0
        self.name                        = ""
        self.cmd                         = ""
        self.CastOn                      = 0
        self.Class                       = 0
        self.duration                    = 0
        self.durationEffect              = False
        self.effects                     = {}
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
        # If it is an instant spell remove it from player
        # If it isn't, begin counting down timeleft of it's duration
        if self.duration == 0:
            player.effectingSpell = 0
        else:
            self.timeleft = self.duration - 1

        # Apply the stat changes
        ApplyStats(player)

        # Does he make a guesture or pick it up?  If so, tell everyone
        if self.guesture[0] != "*":
            player.sendToPlayer( self.guesture[0] % (amDefines.BLUE, amDefines.WHITE) )
            player.sendToRoom( self.guesture[1] % (amDefines.BLUE, player.name, amDefines.WHITE) )


        # Tell everyone
        if self.casted == 1:
            if player == caster:
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
        if self.timeleft == 0:
            RemoveSpell(player)

            return
        
        # Create allbuffs list and append all currently applied spells (good and bad)
        allbuffs = []
        allbuffs.append(player.GoodBuffs)
        allbuffs.append(player.NegBuffs)
        
        # Apply the stat changes for each spell
        for spell in allbuffs:
            # If the spell is an EoT spell, apple the effects
            if spell.durationEffect == True:
                for (stat, value) in self.effects.items():
                    if stat == HP:
                        if (player.hp + value) > player.maxhp:
                            player.hp = player.maxhp
                        else:
                            player.hp += value
                    
        # Tell player about effects if exist
        if self.effectText != "*":
            player.sendToPlayer( self.effectText % (amDefines.BLUE, amDefines.WHITE) )


    ##############################################################
    # ApplySpell()
    #
    # Apply stats
    ##############################################################
    def ApplySpell(self, player):
       # Apply Stat changes
        for (stat, val) in self.effects.values():
            if stat == HP:
                player.hp += val
            elif stat == MAXHP:
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
    # RemoveSpellEffects()
    #
    # Remove the spell and tell the player it wore off
    ##############################################################
    def RemoveSpellEffects(self, player):
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