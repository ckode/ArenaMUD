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

SpawnItems  = {}
SpellList   = {}

HP          = 1
MAXHP       = 2



class Spells():
    def __init__(self):
        self.id                          = 0
        self.name                        = ""
        self.cmd                         = ""
        self.casted                      = 0
        self.targets                     = 0
        self.reqClass                    = []
        self.duration                    = 0
        self.timeleft                    = 0
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

        # Apply the stat changes
        ApplyStats(player)

        player.sendToPlayer( self.effectText % (amDefines.BLUE, amDefines.WHITE) )


    ##############################################################
    # ApplyStats()
    #
    # Apply stats
    ##############################################################
    def ApplyStats(self, player):
       # Apply Stat changes
        for (stat, val) in self.effects.values():
           if stat == HP:
               player.hp += val
           elif stat == MAXHP:
               player.maxhp += val

    ##############################################################
    # RemoveSpell()
    #
    # Remove the spell and tell the player it wore off
    ##############################################################
    def RemoveSpell(self, player):
        player.effectingSpell = 0
        player.maxhp = player.staticmaxhp

        player.sendToPlayer( self.WearOffText % (amDefines.BLUE, amDefines.WHITE) )