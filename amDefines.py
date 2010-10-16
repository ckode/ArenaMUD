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

import string
# Game player status defines
LOGOUT           = 0
LOGIN            = 1
GETNAME          = 2
PLAYING          = 3
GETPASSWORD      = 4
COMPAREPASSWORD  = 5
NEW              = 6
GETCLASS         = 7
GETRACE          = 8
PURGATORY        = 9
EDIT             = 50

# All allowable printable characters (and BACKSPACE!)
PRINTABLE_CHARS = string.printable + chr(0x08)

#############ANSI defines################
#          Foreground Colors
RESET              = chr(27) + "[0m"
BOLD               = chr(27) + "[1m"
ITALIC             = chr(27) + "[3m"
UNDERLINE          = chr(27) + "[4m"
INVERSE            = chr(27) + "[7m"
STRIKE             = chr(27) + "[9m"
BOLD_OFF           = chr(27) + "[22m"
ITALIC_OFF         = chr(27) + "[23m"
UNDERLINE_OFF      = chr(27) + "[24m"
INVERSE_OFF        = chr(27) + "[27m"
STRIKE_OFF         = chr(27) + "[29m"
BLACK              = chr(27) + "[30m"
RED                = chr(27) + "[31m"
GREEN              = chr(27) + "[32m"
BROWN              = chr(27) + "[33m"
YELLOW             = chr(27) + "[1;33m"
BLUE               = chr(27) + "[34m"
MAGENTA            = chr(27) + "[35m"
CYAN               = chr(27) + "[36m"
WHITE              = chr(27) + "[37m"
DEFAULT            = chr(27) + "[39m"
#        Light Foreground Colors
LRED               = chr(27) + "[1;31m"
LGREEN             = chr(27) + "[1;32m"
LBLUE              = chr(27) + "[1;34m"
LMAGENTA           = chr(27) + "[1;35m"
LCYAN              = chr(27) + "[1;36m"
#          Background Colors
B_BLACK            = chr(27) + "[40m"
B_RED              = chr(27) + "[41m"
B_GREEN            = chr(27) + "[42m"
B_YELLOW           = chr(27) + "[43m"
B_BLUE             = chr(27) + "[44m"
B_MAGENTA          = chr(27) + "[45m"
B_CYAN             = chr(27) + "[46m"
B_WHITE            = chr(27) + "[47m"
B_DEFAULT          = chr(27) + "[49m"

#          Cursor and delete line
DELETELINE         = chr(27) + "[2K"
FIRSTCOL           = chr(27) + "[80D"
CURPOS             = chr(27) + "6n"
SAVECUR            = chr(27) + "s"
RESTORECUR         = chr(27) + "r"
DELETELEFT         = chr(27) + "[1K"

#          Light Levels
NORMALVISION       = 1
NIGHTVISION        = 2
DARKVISION         = 3

#          Directions
NORTH              = 1
NE                 = 2
EAST               = 3
SE                 = 4
SOUTH              = 5
SW                 = 6
WEST               = 7
NW                 = 8
UP                 = 9
DOWN               = 10

DIRECTIONS         = ['north', 'ne', 'northeast', 'east', 'se', 'southeast', 'south',
                      'sw', 'southwest', 'west', 'nw', 'northwest', 'up', 'down' ]

########### Command Numbers #############
COMMANDS =       { '/quit':        0,
                   'who':          1,
                   'gossip':       2,
                   'say':          3,
                   'emote':        4,
                   'help':         5,
                   'set password': 6,
                   'set lastname': 7,
                   'look':         8,
                   'rofl':         9,
                   'wtf':         10,
                   'slap':        11
                 }

########### Command List ################
COMMAND_DEFS  = { 0:            "Disconnect from the game.",
                  1:            "Who is in the game.",
                  2:            "Used to gossip to everyone in the game.",
                  3:            "Use to say something or just type your mesage.",
                  4:            "Used to make your own action.",
                  5:            "Command used to list commands.",
                  6:            "Change password: 'set password <password>'",
                  7:            "Change lastname: 'set lastname <lastname>'",
                  8:            "Allows you to look around the room.",
                  9:            "An action",
                 10:            "An action",
                 11:            "slap <person>"
                }

STATS_ABILITIES = { 0:            "Armor Class",
                    1:            "Damage Resistance",
                    2:            "Magic Resistance",
                    3:            "Strength",
                    4:            "Intelligence",
                    5:            "Wisdom",
                    6:            "Agility",
                    7:            "Charm",
                    8:            "Health",
                    9:            "Mana",
                   10:            "Spell Casting",
                   11:            "Stealth",
                   12:            "Perception",
                   13:            "Minimum Damage",
                   14:            "Maximum Damage",
                   15:            "Backstab Damage",
                   16:            "Backstab Accuracy",
                   17:            "Fire Resistance",
                   18:            "Cold Resistance",
                   19:            "Night Vision",
                   20:            "Dark Vision"
                  };
