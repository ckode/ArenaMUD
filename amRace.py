#  ArenaMUD - A multiplayer combat game - http://arenamud.david-c-brown.com
#  Copyright (C) 2010 - David C Brown & Mark Richardson
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


# List of all races
RaceList = {}
###################################
# am Race class
###################################
class Race():
   def __init__(self):
       self.id               = 0
       self.name             = ""
       self.desc             = 0      # TextBlock ID
       self.basehp           = 0
       self.damagebonus      = 0
       self.castingbonus     = 0
       self.vision           = 0
       self.defensebonus     = 0
       self.attackbonus      = 0
       self.stealth          = 0





# List of all races
ClassList = {}
###################################
# am Race class
###################################
class Class():
   def __init__(self):
       self.id               = 0
       self.name             = ""
       self.desc             = ""      # TextBlock ID
       self.hpBonus          = 0
       self.mindamage        = 0
       self.maxdamage        = 0
       self.BaseArmor        = 0
       self.MageryType       = 0
       self.stealth          = 0
       self.weapontext       = 0


