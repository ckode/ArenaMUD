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

import amDefines, amDB, amLog, amCommands
import amRooms, amUtils, amParser, amRace
import amMaps, amSpells, amCombat

import time, re, random, textwrap

#Help topics
HelpTopics = { "race":          "General help and list of races available.",
               "class" :        "General help and list of classses available.",
               "commands" :     "General help and lising of available commands.",
               "movement" :     "General help about how to move around the world.",
               "spells" :       "General help topics listing for spells.",
               "skills" :       "General help topics listing for skills."
               
}

############################################################
# HelpParser
# give the correct help topics
############################################################
def HelpParser(player,cmd):
    
    objList = cmd.split()[0]
    topic = re.compile(re.escape(objList.lower()))
  
    for each in HelpTopics.keys():
        if topic.match(each):
            if each == "race":
                RaceHelp(player)
                return
            elif each == "class":
                player.transport.write("%sYou have chosen help on the class topic. It is not yet available.\n\r" % (amDefines.LCYAN))
                return
            elif each == "commands":
                CommandHelp(player)
                return
            elif each == "movement":
                player.transport.write("%sYou have chosen help on the movement topic. It is not yet available.\n\r" % (amDefines.LCYAN))
                return
            elif each == "spells":
                player.transport.write("%sYou have chosen help on the spell topic. It is not yet available.\n\r" % (amDefines.LCYAN))
                return
            elif each == "skills":
                player.transport.write("%sYou have chosen help on the skill topic. It is not yet available.\n\r" % (amDefines.LCYAN))
                return
    player.transport.write("%sThere is no help on the %s topic.%s\n\r" % (amDefines.LCYAN, cmd, amDefines.WHITE))
    return

############################################################
# RaceHelp function
# sees what race the caller wants info for and outputs it
############################################################
def RaceHelp(player):
    
    player.transport.write("\n\r%s=-=-=-=-=-=-=-=-=-= %sArenaMUD Race Help%s =-=-=-=-=-=-=-=-=-=%s\n\r\n\r" % ( amDefines.LGREEN, amDefines.LRED, amDefines.LGREEN, amDefines.YELLOW))
    
    player.transport.write("  ArenaMUD Currently offers the following races for play.\n\r  Each race has different abilities and skills that can be\n\r  combined with class selections to form a customized\n\r  character.\n\r\n\r")
    
    for Key, Value in amRace.RaceList.items():
        player.transport.write("%s%s %s%s\r\n" % (amDefines.LCYAN, Value.name.ljust(10,' '), amDefines.YELLOW, Value.desc.ljust(50,' ')))
    
    player.transport.write("\n\r%s  Type help %s<race>%s for race specific information.%s\r\n" %(amDefines.YELLOW, amDefines.LCYAN, amDefines.YELLOW, amDefines.WHITE))
    player.transport.write("%s=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=%s\r\n" % ( amDefines.LGREEN, amDefines.WHITE))
    amUtils.StatLine(player)
    return        

############################################################
# GeneralHelpTopics(player)
############################################################
def GeneralHelpTopics(player):
    
    player.transport.write("\n\r%s=-=-=-=-=-=-=-=-=-= %sArenaMUD Help Topics%s =-=-=-=-=-=-=-=-=-=%s\n\r\n\r" % ( amDefines.LGREEN, amDefines.LRED, amDefines.LGREEN, amDefines.YELLOW))
    
    player.transport.write("  Welcome to %sArenaMUD %s%s help topics screen. Available \n\r  help topics are listed below:\n\r\n\r" % (amDefines.LRED, amDefines.SERVER_VERSION, amDefines.YELLOW))
    
    for Key, Value in HelpTopics.iteritems():
        player.transport.write("%s%s %s%s\r\n" % (amDefines.LCYAN, Key.ljust(10,' '), amDefines.YELLOW, Value.ljust(50,' ')))
    
    player.transport.write("\n\r%s  Type help %s<topic>%s for help on one of the listed topics.%s\r\n" %(amDefines.YELLOW, amDefines.LCYAN, amDefines.YELLOW, amDefines.WHITE))
    player.transport.write("%s=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=%s\r\n" % ( amDefines.LGREEN, amDefines.WHITE))
    amUtils.StatLine(player)
    return

############################################################
# CommandHelp function
# List the available commands to the user
############################################################
def CommandHelp(player):
    
    titleLine = "{0}ArenaMUD {1} Command Help{2}".format(amDefines.LRED, amDefines.SERVER_VERSION, amDefines.YELLOW)
    blankLine = "\n\r{0}{1:64}{2}".format(amDefines.BOX_SIDE_DOUBLE, '', amDefines.BOX_SIDE_DOUBLE)
    line1 = "\n\r{0:<1s}{1:<1s}{2:\xCD^78s}{3:>1s}".format(amDefines.YELLOW,amDefines.BOX_TOP_LEFT, titleLine, amDefines.BOX_TOP_RIGHT)
    line2 = "\n\r{0:<1}{1:>15} {2:<48}{3:1}".format(amDefines.BOX_SIDE_DOUBLE, "Command1", "Brief description of the command in question", amDefines.BOX_SIDE_DOUBLE)
    line3 = "\n\r{0:<1}{1:\xCD^64}{2:1}{3:1}\n\r".format(amDefines.BOX_BOTTOM_LEFT, amDefines.BOX_DOUBLE_LINE, amDefines.BOX_BOTTOM_RIGHT, amDefines.WHITE)
    line4 = "\n\r{0:<1}{1:>15} {2:<48}{3:1}".format(amDefines.BOX_SIDE_DOUBLE, "Command2", "Description of the other command in question", amDefines.BOX_SIDE_DOUBLE)
    
    player.transport.write(line1)
    player.transport.write(blankLine)
    player.transport.write(line2)
    player.transport.write(line4)
    player.transport.write(blankLine)
    player.transport.write(line3)
    amUtils.StatLine(player)
    return
