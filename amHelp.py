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
                ClassHelp(player)
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
        player.transport.write("  %s%s %s%s\r\n" % (amDefines.LCYAN, Value.name.ljust(10,' '), amDefines.YELLOW, Value.desc.ljust(50,' ')))
    
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
        player.transport.write("  %s%s %s%s\r\n" % (amDefines.LCYAN, Key.ljust(10,' '), amDefines.YELLOW, Value.ljust(50,' ')))
    
    player.transport.write("\n\r%s  Type help %s<topic>%s for help on one of the listed topics.%s\r\n" %(amDefines.YELLOW, amDefines.LCYAN, amDefines.YELLOW, amDefines.WHITE))
    player.transport.write("%s=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=%s\r\n" % ( amDefines.LGREEN, amDefines.WHITE))
    amUtils.StatLine(player)
    return

############################################################
# CommandHelp function
# List the available commands to the user
############################################################
def CommandHelp(player):
    
    titleText = " {0}ArenaMUD {1} Command Help{2} ".format(amDefines.LRED, amDefines.SERVER_VERSION, amDefines.LGREEN)
    blankLine = "\n\r{0}{1:64}{2}".format(amDefines.BOX_SIDE_DOUBLE, '', amDefines.BOX_SIDE_DOUBLE)
    topLine = "\n\r{0}{1}{2:\xCD^78}{3}".format(amDefines.LGREEN,amDefines.BOX_TOP_LEFT, titleText, amDefines.BOX_TOP_RIGHT)
    bottomLine = "\n\r{0}{1}{2:\xCD^64}{3:1}{4:1}\n\r".format(amDefines.LGREEN, amDefines.BOX_BOTTOM_LEFT, amDefines.BOX_DOUBLE_LINE,
                                                              amDefines.BOX_BOTTOM_RIGHT, amDefines.WHITE)
    
    player.transport.write(topLine + blankLine)
    
    for key in amParser.commands.keys():
        displayStr = "\n\r{0}{1:<1}  {2}{3:<13} {4}{5:<48}{6}{7:1}".format(amDefines.LGREEN, amDefines.BOX_SIDE_DOUBLE, amDefines.LCYAN, key,
                                                                  amDefines.YELLOW, "Sample brief decription of command.",
                                                                  amDefines.LGREEN, amDefines.BOX_SIDE_DOUBLE)
        player.transport.write(displayStr)
        
    player.transport.write(bottomLine)
    amUtils.StatLine(player)
    return

############################################################
# classHelp function
# List the available classes to the user
############################################################
def ClassHelp(player):
    
    titleText = " {0}ArenaMUD {1} Class Help{2} ".format(amDefines.LRED, amDefines.SERVER_VERSION, amDefines.LGREEN)
    blankLine = "\n\r{0}{1:64}{2}".format(amDefines.BOX_SIDE_DOUBLE, '', amDefines.BOX_SIDE_DOUBLE)
    topLine = "\n\r{0}{1}{2:\xCD^78}{3}".format(amDefines.LGREEN,amDefines.BOX_TOP_LEFT, titleText, amDefines.BOX_TOP_RIGHT)
    bottomLine = "\n\r{0}{1}{2:\xCD^64}{3:1}{4:1}\n\r".format(amDefines.LGREEN, amDefines.BOX_BOTTOM_LEFT, amDefines.BOX_DOUBLE_LINE,
                                                              amDefines.BOX_BOTTOM_RIGHT, amDefines.WHITE)
    
    player.transport.write(topLine + blankLine)
    
    for Key, Value in amRace.ClassList.items():
        displayStr = "\n\r{0}{1:<1}  {2}{3:<13} {4}{5:<48}{6}{7:1}".format(amDefines.LGREEN, amDefines.BOX_SIDE_DOUBLE, amDefines.LCYAN, Value.name,
                                                                  amDefines.YELLOW, Value.desc, amDefines.LGREEN, amDefines.BOX_SIDE_DOUBLE)
        player.transport.write(displayStr)
    
    displayStr = "\n\r{0}{1}{2}{3:^64}{4}{5}".format( amDefines.LGREEN, amDefines.BOX_SIDE_DOUBLE, amDefines.YELLOW,
                                                      "Type help <class> for class specific information.", amDefines.LGREEN,
                                                      amDefines.BOX_SIDE_DOUBLE)
    player.transport.write( blankLine + displayStr + blankLine)
    player.transport.write(bottomLine)
    amUtils.StatLine(player)
    return