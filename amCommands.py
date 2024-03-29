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

from twisted.internet import reactor

import amDefines, amDB, amLog, amCommands
import amRooms, amUtils, amParser, amRace
import amMaps, amSpells, amCombat

import time, re, random, textwrap


NONE         =  0
NORTH        =  1
NE           =  2
EAST         =  3
SE           =  4
SOUTH        =  5
SW           =  6
WEST         =  7
NW           =  8
UP           =  9
DOWN         = 10

ATTACKING               = 0
CASTING                 = 1
SKILL                   = 2


MOVINGTEXT = {  1: " leaves to the north.| arrives from the south.",
                2: " leaves to the northeast.| arrives from the southwest.",
                3: " leaves to the east.| arrives from the west.",
                4: " leaves to the southeast.| arrives from the northwest.",
                5: " leaves to the south.| arrives from the north.",
                6: " leaves to the southwest.| arrives from the northeast.",
                7: " leaves to the west.| arrives from the east.",
                8: " leaves to the northwest.| arrives from the southeast.",
                9: " leaves up .| arrives from below.",
               10: " leaves down.| arrives from above.",
             }

SNEAKINGTEXT = {  1: " sneaking out to the north.| sneaking in from the south.",
                  2: " sneaking out to the northeast.| sneaking in from the southwest.",
                  3: " sneaking out to the east.| sneaking in from the west.",
                  4: " sneaking out to the southeast.| sneaking in from the northwest.",
                  5: " sneaking out to the south.| sneaking in from the north.",
                  6: " sneaking out to the southwest.| sneaking in from the northeast.",
                  7: " sneaking out to the west.| sneaking in from the east.",
                  8: " sneaking out to the northwest.| sneaking in from the southeast.",
                  9: " sneaking out up .| sneaking in from below.",
                 10: " sneaking out down.| sneaking in from above.",
             }

################################################
# MovePlayer() function
################################################
def MovePlayer(player, Direction):
   global RoomList
   FailedSneak = False
   player.resting = False

   # Did player die before movement happen? Abort if in Purgatory
   if player.STATUS == amDefines.PURGATORY:
      return

   # If the player is held or stun, he can't move!
   if player.held:
      player.moving = 0
      player.sendToPlayer("You cannot move!")
      player.sendToRoomNotVictim( player.playerid, "%s%s struggles to move!" % (amDefines.YELLOW, player.name) )
      return
   elif player.stun:
      player.moving = 0
      player.sendToPlayer("You stumble about dazedly and cannot move!")
      player.sendToRoomNotVictim( player.playerid, "%s%s stumbles about dazedly!" % (amDefines.WHITE, player.name) )
      return
   
   amUtils.StatLine(player)

   # Sub function that can be called when a player's path is blocked.
   def RunIntoWall(PassageType, playerName):
      theDir = amRooms.DIRTEXT[Direction]

      ToPlayer = "You run into the %s %s!" % (PassageType, theDir)
      ToRoom = "%s runs into the %s %s!" % (player.name, PassageType, theDir)
      player.sendToPlayer("%s%s%s" % (amDefines.BLUE, ToPlayer, amDefines.WHITE) )
      player.sendToRoom("%s%s%s" % (amDefines.WHITE, ToRoom, amDefines.WHITE) )
      amUtils.StatLine(player)

   # Is the door in a passable state?
   if amMaps.Map.Rooms[player.room].Doors.has_key(Direction):
      CurDoorNum = amMaps.Map.Rooms[player.room].Doors[Direction]
      if amMaps.Map.Doors[CurDoorNum].Passable == True:
         if player.sneaking == True:
            if random.randint(1, 100) > player.stealth:
               SNEAKING = SNEAKINGTEXT[Direction].split('|')
               FailedSneak = True
               player.sendToRoom("%sYou noticed %s%s" % (amDefines.LRED, player.name,  SNEAKING[0]))
               player.sendToPlayer("%sYou make a sound enter the room!%s" % (amDefines.LRED, amDefines.WHITE))

         # Get new room's room number, remove player from old room.
         NewRoom = amMaps.Map.Doors[CurDoorNum].ExitRoom[player.room]

         del amMaps.Map.Rooms[player.room].Players[player.playerid]


         # Set players room num in his profile and tell room he left
         MOVING = MOVINGTEXT[Direction].split('|')
         if player.sneaking == False:
            player.sendToRoom(amDefines.WHITE + player.name + MOVING[0])
         player.room = NewRoom

         # Add player to that room and tell everyone
         amMaps.Map.Rooms[NewRoom].Players[player.playerid] = player.name
         # Sneaking in message
         if player.sneaking:
            if FailedSneak == True:
               player.sneaking = False
               player.sendToRoom( "%sYou noticed %s%s" % (amDefines.LRED, player.name, SNEAKING[1]) )
         else:
            player.sendToRoom(amDefines.WHITE + player.name + MOVING[1])

         # Is there a trap room trap in the room? Spring it!
         if amMaps.Map.Rooms[NewRoom].RoomTrap > 0:
            amUtils.SpringRoomTrap(player, amMaps.Map.Rooms[NewRoom].RoomTrap)
            player.sneaking = False
            # Did the player die from a trap? If so, don't continue, just return
            if player.STATUS == amDefines.PURGATORY:
               player.moving = False
               return
         
         # Show the player the room he/she just entered if he didn't die from a trap
         amCommands.Look(player, player.room, player.briefDesc)
      else:
         # There is a doorway, but it's not passable
         PassageType = amUtils.MessageList[amMaps.Map.Doors[CurDoorNum].DoorDesc].split('|')[0]
         player.sneaking = False
         RunIntoWall(PassageType, player.name)
   else:
      # There is no door, just a wall.
      RunIntoWall("wall", player.name)
      player.sneaking = False

   player.moving = 0


################################################
# Command Up
################################################
def Up(player):
   MovePlayer(player, UP)
   return

################################################
# Command Down
################################################
def Down(player):
   MovePlayer(player, DOWN)
   return

################################################
# Command North
################################################
def North(player):
   MovePlayer(player, NORTH)
   return

################################################
# Command NorthEast
################################################
def NorthEast(player):
   MovePlayer(player, NE)
   return

################################################
# Command East
################################################
def East(player):
   MovePlayer(player, EAST)
   return

################################################
# Command SouthEast
################################################
def SouthEast(player):
   MovePlayer(player, SE)
   return

################################################
# Command South
################################################
def South(player):
   MovePlayer(player, SOUTH)
   return
################################################
# Command SouthWest
################################################
def SouthWest(player):
   MovePlayer(player, SW)
   return

################################################
# Command West
################################################
def West(player):
   MovePlayer(player, WEST)
   return

################################################
# Command NorthWest
################################################
def NorthWest(player):
   MovePlayer(player, NW)
   return

################################################
# Command -> QUIT
################################################
def Quit(player):
   player.disconnectClient()

################################################
# Command -> Open
################################################
def Open(player, something):
   global DIRECTIONS
   
   objList = something.split()[0]
   obj = re.compile(re.escape(objList.lower()))
   # Only doors exist now
   if obj.match('north'):
      OpenDoor(player, NORTH)
      return
   elif obj.match('ne') and len(objList) == 2 or obj.match('northeast') and len(objList) > 5:
      OpenDoor(player, NE)
      return
   elif obj.match('east'):
      OpenDoor(player, EAST)
      return
   elif obj.match('se') and len(objList) == 2 or obj.match('southeast') and len(objList) > 5:
      OpenDoor(player, SE)
      return
   elif obj.match('south'):
      OpenDoor(player, SOUTH)
      return
   elif obj.match('sw') and len(objList) == 2 or obj.match('southwest') and len(objList) > 5:
      OpenDoor(player, SW)
      return
   elif obj.match('west'):
      OpenDoor(player, WEST)
      return
   elif obj.match('nw') and len(objList) == 2 or obj.match('northwest') and len(objList) > 5:
      OpenDoor(player, NW)
      return
   elif obj.match('up'):
      OpenDoor(player, UP)
      return
   elif obj.match('down'):
      OpenDoor(player, DOWN)
      return

################################################
# Command -> Close
################################################
def Close(player, something):
   global DIRECTIONS

   player.resting = False
   amUtils.StatLine(player)
   objList = something.split()[0]
   obj = re.compile(re.escape(objList.lower()))
   # Only doors exist now
   if obj.match('north'):
      CloseDoor(player, NORTH)
      return
   elif obj.match('ne') and len(objList) == 2 or obj.match('northeast') and len(objList) > 5:
      CloseDoor(player, NE)
      return
   elif obj.match('east'):
      CloseDoor(player, EAST)
      return
   elif obj.match('se') and len(objList) == 2 or obj.match('southeast') and len(objList) > 5:
      CloseDoor(player, SE)
      return
   elif obj.match('south'):
      CloseDoor(player, SOUTH)
      return
   elif obj.match('sw') and len(objList) == 2 or obj.match('southwest') and len(objList) > 5:
      CloseDoor(player, SW)
      return
   elif obj.match('west'):
      CloseDoor(player, WEST)
      return
   elif obj.match('nw') and len(objList) == 2 or obj.match('northwest') and len(objList) > 5:
      CloseDoor(player, NW)
      return
   elif obj.match('up'):
      CloseDoor(player, UP)
      return
   elif obj.match('down'):
      CloseDoor(player, DOWN)
      return

################################################
# Command -> Bash
################################################
def Bash(player, something):
   global DIRECTIONS

   objList = something.split()[0]
   obj = re.compile(re.escape(objList.lower()))
   # Only doors exist now
   if obj.match('north'):
      BashDoor(player, NORTH)
      return
   elif obj.match('ne') and len(objList) == 2 or obj.match('northeast') and len(objList) > 5:
      BashDoor(player, NE)
      return
   elif obj.match('east'):
      BashDoor(player, EAST)
      return
   elif obj.match('se') and len(objList) == 2 or obj.match('southeast') and len(objList) > 5:
      BashDoor(player, SE)
      return
   elif obj.match('south'):
      BashDoor(player, SOUTH)
      return
   elif obj.match('sw') and len(objList) == 2 or obj.match('southwest') and len(objList) > 5:
      BashDoor(player, SW)
      return
   elif obj.match('west'):
      BashDoor(player, WEST)
      return
   elif obj.match('nw') and len(objList) == 2 or obj.match('northwest') and len(objList) > 5:
      BashDoor(player, NW)
      return
   elif obj.match('up'):
      BashDoor(player, UP)
      return
   elif obj.match('down'):
      BashDoor(player, DOWN)
      return


################################################
# Command -> BashDoor
################################################
def BashDoor(player, DIRECTION):
   global RoomList, DIRTEXT
   CurDoorID = amMaps.Map.Rooms[player.room].GetDoorID(DIRECTION)

   if CurDoorID == 0:
      # Door doesn't exist.
      player.sendToPlayer("%s%s%s" % (amDefines.WHITE, "You do not see anything to bash ", amRooms.DIRTEXT[DIRECTION]) )
      return

   OtherRoomID = amMaps.Map.Doors[CurDoorID].GetOppositeRoomID(player.room)
   CurDoor = amMaps.Map.Doors[CurDoorID]


   if CurDoor.Passable:
      player.sendToPlayer("%s%s is already open." % (amDefines.WHITE, amRooms.DIRTEXT[DIRECTION].capitalize()) )
   else:
      # Is this a door and is it visable?
      if CurDoor.DoorType == 2 or CurDoor.DoorType == 4:

         # You can't attack/rest and bash at the same time.
         player.resting = False
         if player.attacking == True:
            player.factory.CombatQueue.RemoveAttack(player.playerid)
            player.attacking = False
            player.victim = ""
            player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE))
            player.sendToRoom("%s%s breaks off combat.%s" % (amDefines.BROWN, player.name, amDefines.WHITE))

         # Open the door on both sides of the door.
         amMaps.Map.Doors[CurDoorID].Passable = True
         amMaps.Map.Doors[CurDoorID].DoorStatus = amRooms.OPEN
         
         player.sendToPlayer("%sYou bash the %s to the %s open!" % (amDefines.WHITE, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[DIRECTION]) )
         player.sendToRoom("%s%s bashes the %s to the %s open!" % (amDefines.WHITE, player.name, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[DIRECTION]) )
         player.BroadcastToRoom("%sThe %s to the %s flies open!" % (amDefines.WHITE, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[amRooms.OPPOSITEDOOR[DIRECTION]]), OtherRoomID)
      else: # You don't see a door!
         player.sendToPlayer("%s%s%s" % (amDefines.WHITE, "You do not see anything to bash open to the ", amRooms.DIRTEXT[DIRECTION]) )



################################################
# Command -> OpenDoor
################################################
def OpenDoor(player, DIRECTION):
   global RoomList, DIRTEXT
   CurDoorID = amMaps.Map.Rooms[player.room].GetDoorID(DIRECTION)

   if CurDoorID == 0:
      # Door doesn't exist.
      player.sendToPlayer("%s%s%s" % (amDefines.WHITE, "You do not see anything to close to the ", amRooms.DIRTEXT[DIRECTION]) )
      return

   OtherRoomID = amMaps.Map.Doors[CurDoorID].GetOppositeRoomID(player.room)
   CurDoor = amMaps.Map.Doors[CurDoorID]

   if CurDoor.Passable:
      player.sendToPlayer("%s%s is already open." % (amDefines.WHITE, amRooms.DIRTEXT[DIRECTION].capitalize()) )
   else:
      # Is this a door and is it visable?
      if CurDoor.DoorType == 2 or CurDoor.DoorType == 4:

         # You can't attack/rest and open a door at the same time.
         player.resting = False
         if player.attacking == True:
            player.factory.CombatQueue.RemoveAttack(player.playerid)
            player.attacking = False
            player.victim = ""
            player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE))
            player.sendToRoom("%s%s breaks off combat.%s" % (amDefines.BROWN, player.name, amDefines.WHITE))
         # If locked, say so
         if CurDoor.Locked == 1:
            player.sendToPlayer("%s%s%s" % (amDefines.WHITE, amRooms.DIRTEXT[DIRECTION].capitalize(), " is locked.") )
         else:
            CurDoor.DoorType == 2 or CurDoor.DoorType == 4
            # Open the door on both sides of the door.
            amMaps.Map.Doors[CurDoorID].Passable = True
            amMaps.Map.Doors[CurDoorID].DoorStatus = amRooms.OPEN
            player.BroadcastToRoom("%sThe %s to the %s opens." % (amDefines.WHITE, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[amRooms.OPPOSITEDOOR[DIRECTION]]), OtherRoomID)
            player.sendToPlayer("%sYou open the %s to the %s." % (amDefines.WHITE, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[DIRECTION]) )
            player.sendToRoom("%s%s opens the %s to the %s." % (amDefines.WHITE, player.name, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[DIRECTION]) )
      else: # You don't see a door!
         player.sendToPlayer("%s%s%s" % (amDefines.WHITE, "You do not see anything to open to the ", amRooms.DIRTEXT[DIRECTION]) )

################################################
# Command -> CloseDoor
################################################
def CloseDoor(player, DIRECTION):
   global RoomList, DIRTEXT

   CurDoorID = amMaps.Map.Rooms[player.room].GetDoorID(DIRECTION)
   if CurDoorID == 0:
      # Door doesn't exist.
      player.sendToPlayer("%s%s%s" % (amDefines.WHITE, "You do not see anything to close to the ", amRooms.DIRTEXT[DIRECTION]) )
      return
   OtherRoomID = amMaps.Map.Doors[CurDoorID].GetOppositeRoomID(player.room)
   CurDoor = amMaps.Map.Doors[CurDoorID]

   # Is this a door of type door or gate? (need to fix this so I just check 1 thing)
   if CurDoor.DoorType == 2 or CurDoor.DoorType == 4:
      if CurDoor.Passable == False:
         player.sendToPlayer("%s%s is already closed." % (amDefines.WHITE, amRooms.DIRTEXT[DIRECTION].capitalize()) )
      else:
         # You can't attack/rest and close a door at the same time.
         player.resting = False
         if player.attacking == True:
            player.factory.CombatQueue.RemoveAttack(player.playerid)
            player.attacking = False
            player.victim = ""
            player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE))
            player.sendToRoom("%s%s breaks off combat.%s" % (amDefines.BROWN, player.name, amDefines.WHITE))

             # Close the door
         amMaps.Map.Doors[CurDoorID].Passable = False
         amMaps.Map.Doors[CurDoorID].DoorStatus = amRooms.CLOSED
      
         player.sendToPlayer("%sYou close the %s to the %s." % (amDefines.WHITE, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[DIRECTION]) )
         player.sendToRoom("%s%s closes the %s to the %s." % (amDefines.WHITE, player.name, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[DIRECTION]) )
         player.BroadcastToRoom("%sThe %s to the %s closes." % (amDefines.WHITE, amRooms.DOORTYPE[CurDoor.DoorType], amRooms.DIRTEXT[amRooms.OPPOSITEDOOR[DIRECTION]]), OtherRoomID)
   else:
      # You don't see a door!
      player.sendToPlayer("%s%s%s" % (amDefines.WHITE, "You do not see anything to close to the ", amRooms.DIRTEXT[DIRECTION]) )


################################################
# Command -> Gossip
################################################
def Gossip(player, line):
   if player.STATUS == amDefines.PLAYING:
      player.Shout(amDefines.MAGENTA + player.name + " gossips: " + line)
   else:
      player.Shout(amDefines.MAGENTA + player.name + " gossips (purgatory): " + line)

      
#===============================================
# WhoCmd
#===============================================
def WhoCmd( player ):
   player.sendToPlayer("%s>> Current Map: %s%s" % (amDefines.GREEN, amDefines.LCYAN, amMaps.Map.MapInfo[0]) )
   Who( player )
   return
################################################
# Command -> Who
################################################
def Who(player):
   global RaceList
   global ClassList
   
   player.sendToPlayer("%s<<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= %sWhos Online%s =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>>" % (amDefines.LCYAN, amDefines.LMAGENTA, amDefines.LCYAN))
   player.sendToPlayer("%s    Warrior         Race            Class           Kills   Deaths   K/D Ratio" % (amDefines.LGREEN))
   for user in player.factory.players.values():
      if user.STATUS == amDefines.PLAYING or user.STATUS == amDefines.PURGATORY:
         try:
            ratio = "%.2f" % ( float(user.kills) / float(user.deaths) )
         except:
            if user.kills == 0:
               ratio = "%.2f" % float(0.00)
            else:
               ratio = "%.2f" % (user.kills)

         if user.STATUS == amDefines.PURGATORY:
            playercolor = amDefines.LRED
         else:
            playercolor = amDefines.LMAGENTA
         
         player.sendToPlayer("%s => %s%s%s %s %s %s  %s    %s" % (amDefines.LCYAN, playercolor, user.name.ljust(15, ' '), amDefines.LCYAN, amRace.RaceList[user.race].name.ljust(15,' '), amRace.ClassList[user.Class].name.ljust(15,' '), str(user.kills).rjust(5, ' '), str(user.deaths).rjust(6, ' '), str(ratio).rjust(9, ' ') ) )

   player.sendToPlayer("%s<<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>>" %(amDefines.LCYAN))
   amUtils.StatLine(player)

################################################
# Command -> Say
################################################
def Say(player, line):
   player.sendToRoom(amDefines.GREEN + player.name + " says: " + amDefines.WHITE + line)
   player.transport.write(amDefines.DELETELEFT)
   player.transport.write(amDefines.FIRSTCOL)
   player.sendToPlayer(amDefines.GREEN + "You say: " + amDefines.WHITE + line + amDefines.WHITE)

################################################
# Command -> Emote
################################################
def Emote(player, line):
   player.sendToRoom(amDefines.BLUE + player.name + " " + line)
   player.sendToPlayer(amDefines.BLUE + player.name + " " + line + amDefines.WHITE)

################################################
# Command -> Brief
################################################
def Brief(player):
   if player.briefDesc == 1:
      player.briefDesc = 0
      player.sendToPlayer(amDefines.WHITE + "Verbose mode set.")
   else:
      player.briefDesc = 1
      player.sendToPlayer(amDefines.WHITE + "Quiet mode set.")

################################################
# Command -> Help
################################################
def Help(player):
   width = 15
   for command in amDefines.COMMANDS.keys():
      fill = width - (len(command) + 1)
      player.sendLine(amDefines.MAGENTA + "   " + " " * fill + command + amDefines.WHITE +  " => " +
                                        amDefines.COMMAND_DEFS[amDefines.COMMANDS[command]])

################################################
# Command -> Slap
################################################
def Slap(player, victim):
   global RoomList
   vict = {}
   if victim == "":
      player.sendToPlayer(amDefines.BLUE + "You slap yourself!")
      player.sendToRoom(amDefines.BLUE + player.name + " slaps himself!")
   else:
      vict = amUtils.FindPlayerInRoom(player, victim)
      if len(vict) == 0:
         return
      else:
         pid    = vict.keys()[0]
         name   = vict.values()[0]
         player.sendToPlayer(amDefines.BLUE + "You slap " + name + "!")
         player.factory.players[pid].sendToPlayer(amDefines.BLUE + player.name + " slaps you!")
         player.sendToRoomNotVictim(pid, amDefines.BLUE + player.name + " slaps " + name + "!")

################################################
# Command -> Crack
################################################
def Crackpipe(player):
   player.sendToRoom(amDefines.GREEN + player.name + " hits the crack pipe hard!" + amDefines.WHITE)
   player.sendToPlayer(amDefines.GREEN + "You hit the crack pipe hard!" + amDefines.WHITE)
################################################
# Command -> Rofl
################################################
def Rofl(player):
   player.sendToRoom(amDefines.GREEN + player.name + " rolls on the floor laughing!" + amDefines.WHITE)
   player.sendToPlayer(amDefines.GREEN + "You roll on the floor laughing!" + amDefines.WHITE)
################################################
# Command -> Say
################################################
def Wtf(player):
   player.sendToRoom(amDefines.GREEN + player.name + " yells, What the fuck!" + amDefines.WHITE)
   player.sendToPlayer(amDefines.GREEN + "You yell, What the fuck!" + amDefines.WHITE)

################################################
# Command -> Sneak
################################################
def Sneak(player):
   player.resting = False
   # If you aren't a stealthy class, or you are attacking, or someone is in the room.  You can't sneak!
   if player.ClassStealth == False or player.attacking == 1 or len(amMaps.Map.Rooms[player.room].Players) > 1:
      player.sendToPlayer("%sYou don't think you're sneaking.%s" % (amDefines.CYAN, amDefines.WHITE))
      player.sneaking = False
      return
   else:
      player.sendToPlayer("%sAttempting to sneak.%s" % (amDefines.WHITE, amDefines.WHITE))
      player.sneaking = True


################################################
# Command -> Look
################################################
def Look(player, RoomNum, DESC):
   global RoomList
   x = 1
   if RoomNum == "":
      RoomNum = player.room
   Room = amMaps.Map.Rooms[RoomNum]
   if player.blind:
      player.sendLine(amDefeines.WHITE + "You are blind!")
      amUtils.StatLine(player)
      return
   if player.vision < Room.LightLevel:
      if Room.LightLevel == amDefines.DARKVISION:
         player.sendLine(amDefines.WHITE + "The room is PITCH BLACK - you can't see anything!")
         amUtils.StatLine(player)
         return
      else:
         player.sendLine(amDefines.WHITE + "The room is too dark, you can't see anything!")
         amUtils.StatLine(player)
         return


   player.sendLine( "%s%s%s%s" % ( amDefines.DELETELEFT, amDefines.FIRSTCOL, amDefines.LCYAN, Room.Name ) )
   if DESC != 1:
      player.sendLine(amDefines.WHITE + Room.Desc1)
      if Room.Desc2 != "*":
         player.sendLine(amDefines.WHITE + Room.Desc2)
      if Room.Desc3 != "*":
         player.sendLine(amDefines.WHITE + Room.Desc3)
      if Room.Desc4 != "*":
         player.sendLine(amDefines.WHITE + Room.Desc4)
      if Room.Desc5 != "*":
         player.sendLine(amDefines.WHITE + Room.Desc5)



   # People in the room
   PeopleInRoom = amUtils.WhoIsInTheRoom(player, RoomNum)
   Count = len(PeopleInRoom)
   if (Count > 1 and player.room == RoomNum) or (Count > 0 and player.room != RoomNum) :
      names = "%sAlso here: %s" % (amDefines.GREEN, amDefines.LMAGENTA)
      for each in PeopleInRoom.values():
         # You don't see yourself!
         if each != player.name:
            if ((Count - 1) > x and player.room == RoomNum) or (Count > x and player.room != RoomNum):
               x += 1
               names = names + each + ", "
            else:
               names = names + each + "." + amDefines.WHITE

      player.sendLine(names)
   
   # Items in the room
   ItemsInRoom = amMaps.Map.Rooms[RoomNum].ItemsYouNotice()
   if ItemsInRoom != None:
      player.sendLine("%sYou notice: %s" % (amDefines.MAGENTA, ItemsInRoom) )

   player.sendToPlayer(Room.DisplayExits() + amDefines.WHITE)
   #amUtils.StatLine(player)
################################################
# Command -> Set <property>
################################################
def Set(player, line):
   parms = line.split()
   if len(parms) > 1:
      property = parms[0]
      value = parms[1]
   else:
      player.sendLine(amDefines.DEFAULT + "Usage: SET <PROPERTY> <VALUE> - type 'help' for more help" + amDefines.WHITE)
      return
   if property.lower() == "lastname":
      if len(value) > 20:
         player.sendLine(amDefines.DEFAULT + "Lastnames limited to 20 characters, try again please." + amDefines.WHITE)
         return
      player.lastname = value.capitalize()
      amDB.ChangeLastname(player.name, value)
      player.sendLine(amDefines.DEFAULT + "Lastname updated." + amDefines.WHITE)
   elif property.lower() == "password":
      if value == "":
         player.sendLine(amDefines.DEFAULT + "Password cannot be blank." + amDefines.WHITE)
         return
      if len(value) > 20:
         player.sendLine(amDefines.DEFAULT + "Passwords limited to 20 characters, try again please." + amDefines.WHITE)
         return
      player.password = value
      amDB.ChangePassword(player.name, value)
      player.sendLine(amDefines.DEFAULT + "Password updated." + amDefines.WHITE)
   else:
      player.sendLine(amDefines.DEFAULT + "Usage: SET <PROPERTY> <VALUE> - type 'help' for more help" + amDefines.WHITE)

#################################################
# Command -> LookAt
#
# This determins what you want to look at
# and then calls the proper function to do it
#################################################
def LookAt(player, lookwhere):

   victimList = amUtils.FindPlayerInRoom(player, lookwhere)

   if len(victimList) > 0 and len(lookwhere) > 1:
      if len(victimList) == 1:
         LookPlayer(player, victimList.keys()[0])
         return
      else:
         player.sendToPlayer("Who did you mean: ")
         for victim in victimList.values():
            player.sendToPlayer(" - " + victim)
         return
   # Is the player trying to look in a direction?
   elif amRooms.DIRLOOKUP.has_key(lookwhere):
      Direction = amRooms.DIRLOOKUP[lookwhere]


      if amMaps.Map.Rooms[player.room].Doors.has_key(Direction):
         CurDoorID = amMaps.Map.Rooms[player.room].GetDoorID(Direction)
         OtherRoomID = amMaps.Map.Doors[CurDoorID].GetOppositeRoomID(player.room)
         _door = amMaps.Map.Rooms[player.room].Doors[Direction]
         # Tell the room you are looking said direction
         player.sendToRoom("%s looks %s" % (player.name, amRooms.DIRTEXT[Direction]))
         # Look into the other room (display)
         Look(player, amMaps.Map.Doors[_door].ExitRoom[player.room], player.briefDesc)
         #tell the room that is being looked into that someone is peeking in
         player.BroadcastToRoom("%s%s peeks in from the %s." % (amDefines.CYAN, player.name, amRooms.DIRTEXT[amRooms.OPPOSITEDOOR[Direction]]), OtherRoomID )
         return
      else:
         player.sendLine("%s%s%s%s" % (amDefines.DEFAULT, "You don't see anything ", amRooms.DIRTEXT[Direction], amDefines.WHITE) )
         amUtils.StatLine(player)
         return
   player.sendLine("You don't see %s here!" % lookwhere)
   amUtils.StatLine(player)
################################################
# Command -> LookPlayer(player, otherplayerID)
################################################
def LookPlayer(player, otherplayerID):
   global RaceList
   global ClassList

   victim = player.factory.players[otherplayerID]

   # If they are sneaking they cant be looked at.
   if victim.sneaking == True:
      player.sendToPlayer("%sYou do not see %s here!" %(amDefines.WHITE, victim.name) )
      return

   player.sneaking = False  #if player looks at another player while sneaking, they aren't sneaking any more.

   if victim.hp < ( ( float(victim.maxhp) / 100) * 25 ):
      HealthStr = "horribly"
      hpcolor = amDefines.LRED
   elif victim.hp < ( ( float(victim.maxhp) / 100) * 50 ):
      HealthStr = "badly"
      hpcolor = amDefines.YELLOW
   elif victim.hp < ( ( float(victim.maxhp) / 100) * 75 ):
      HealthStr = "somewhat"
      hpcolor = amDefines.LGREEN
   elif victim.hp < ( ( float(victim.maxhp) / 100) * 85 ):
      HealthStr = "lightly"
      hpcolor = amDefines.WHITE
   elif victim.hp < ( ( float(victim.maxhp) / 100) * 95 ):
      HealthStr = "barely"
      hpcolor = amDefines.WHITE
   else:
      HealthStr = "not"
      hpcolor = amDefines.WHITE
      
   # If player.hp is higher than maxhp, make it blue (only a buff can do this)
   if victim.hp > victim.maxhp:
      hpcolor = amDefines.BLUE

   player.sendToPlayer("%s<<=-=-=-=-=-=-=-= %s =-=-=-=-=-=-=-=>>" %(amDefines.LCYAN, victim.name))
   player.sendToPlayer("%s%s is a %s %s" %(amDefines.YELLOW, victim.name, amRace.RaceList[victim.race].name, amRace.ClassList[victim.Class].name))
   player.sendToPlayer("%s has %s kills and %s deaths" %(victim.name, str(victim.kills), str(victim.deaths)))
   player.sendToPlayer("%s%s is %s wounded.%s" %(hpcolor, victim.name, HealthStr, amDefines.WHITE))
   
   #if there are any effects the victim is under here is where you can show them
   if victim.stun:
      player.sendToPlayer("%s%s looks completely stunned!" %(amDefines.YELLOW, victim.name))
   elif victim.held:
      player.sendToPlayer("%s%s is held and cannot move!" % (amDefines.YELLOW, victim.name))

   player.sendToRoomNotVictim( victim.playerid, "%s%s looks %s up and down." % (amDefines.WHITE, player.name, victim.name) )
   victim.sendToPlayer( "%s%s looks you up and down." % (amDefines.WHITE, player.name) )

#################################################
# Command -> Attack()
#################################################
def Attack(player, attacked):
   global CombatQueue
   player.resting = False
   amUtils.StatLine(player)

   victimList = amUtils.FindPlayerInRoom(player, attacked)

   # Anybody to attack?
   if len(victimList) == 0:
      player.sendToPlayer("You don't see %s here!" % (attacked,))
   # Was more than one players name matching?
   elif len(victimList) > 1:
      player.sendToPlayer("Fix this, list all possible victims.")
   # Just one, attack!!!
   else:
      victimID = victimList.keys()[0]
      # Don't attack yourself idiot!
      if victimID == player.playerid:
         player.sendToPlayer(amDefines.RED + "Why would you attack yourself idiot!" + amDefines.WHITE)
         return
        # No sneaking after
      player.factory.CombatQueue.AddAttack(player.playerid)
      victim = player.factory.players[victimID]
      player.attacking = 1
      player.victim = victim.playerid
      victim.sneaking = False
      victim.resting = False
      amUtils.StatLine(player)
      player.sendToPlayer("%s*Combat Engaged*%s" %(amDefines.BROWN, amDefines.WHITE))
      if player.sneaking == False:
         victim.sendToPlayer("%s%s moves to attack you!%s" %(amDefines.BROWN, player.name, amDefines.WHITE))
         player.sendToRoomNotVictim(victim.playerid, "%s%s moves to attack %s!%s" % (amDefines.BROWN, player.name, victim.name,  amDefines.WHITE))


#=================================================
# Get()
#
# Get an item in the room (then cast it)
#=================================================
def Get(player, line):
   
   # Get current room
   Room = amMaps.Map.Rooms[player.room]
   
   # Get a list of items in the room
   items = Room.FindItemInRoom( player, line )

   # No items found
   if items == None:
      player.sendToPlayer("%sYou don't see %s here." % (amDefines.WHITE, line) )
      return
   
   # More than one found.
   if len(items) > 1:
      player.sendToPlayer("%sWhich do you mean?" % (amDefines.WHITE) )
      for each in items.keys():
         player.sendToPlayer("%s - %s" % (amDefines.WHITE, each) )
      return
   
   # Apply the items effect to the player
   key = items.keys()[0]
   items[key].ApplyItem( player )
   
   # Now delete the item from the room.
   try:
      del amMaps.Map.Rooms[player.room].Items[key]
   except:
      print "Failed to remove item from room on GET"
      
   # Set the respawn timer!
   amSpells.ReSpawnItemList.append( reactor.callLater(items[key].CoolDown, amUtils.SpawnItem, items[key], player) )
   
   return
         
   
def Rest(player):
   player.resting = True
   if player.attacking == True:
      player.factory.CombatQueue.RemoveAttack(player.playerid)
      player.attacking = False
      player.victim = ""
      player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE))
      player.sendToRoom("%s%s breaks off combat.%s" % (amDefines.BROWN, player.name, amDefines.WHITE))
   player.sendToPlayer("%sYou stop to rest." % (amDefines.WHITE))
   player.sendToRoom("%s%s stops to rest." % (amDefines.WHITE, player.name))

def Break(player):
   player.resting = False

   if player.attacking == True:
      player.factory.CombatQueue.RemoveAttack(player.playerid)
      player.attacking = False
      player.victim = ""
      player.sendToPlayer("%s*Combat Off*%s" % (amDefines.BROWN, amDefines.WHITE))
      player.sendToRoom("%s%s breaks off combat.%s" % (amDefines.BROWN, player.name, amDefines.WHITE))
   amUtils.StatLine(player)
   
##################################################
# Command -> NextMap()
#
# Calls next map in ArenaQueue
##################################################
def NextMap(player):
   global ArenamQueue
   
   
   # Reset kills, deaths, and room
   for user in player.factory.players.values():
      if user.STATUS == amDefines.PLAYING or user.STATUS == amDefines.PURGATORY:
         user.sendToPlayer("Changing map...")
         
   # Move everyone to purgatory
   amUtils.KickAllToPurgatory(player)
   # Switch to the next map
   player.factory.ArenaQueue.LoadNextArena()
   player.Shout( "%sNow playing: %s%s" % (amDefines.GREEN, amDefines.LCYAN, amMaps.Map.MapInfo[0]) )
   
################################################
# Command -> Status(player)
################################################
def Status(player):
   global RaceList
   global ClassList  
   
   # Sub function to left justify text
   def FormatLineLJust( First, Last, Fill ):  
      FirstLen = len(First)
      
      # Check to make sure "First" len() isn't greater than "Fill"
      if FirstLen > Fill:
         amLog.Logit("Error: FormatLineLJust(), 'First' length greater than 'Fill'\r\nFirst = %s, Fill = %i" % (First, Fill) )
         # Just append and send the line back
         return (First + Last)
        
      # Append the appropriate amount of spaces
      fillText = " " * (Fill - FirstLen)
    
      return ( First + fillText + Last )

   
   # Sub function to right justify text
   def FormatLineRJust( First, Last, Fill ):  
      FirstLen = len( First )
      LastLen  = len( Last  )
      
      # Check to make sure "First" len() isn't greater than "Fill"
      if FirstLen > Fill:
         amLog.Logit("Error: FormatLineRJust(), 'First' length greater than 'Fill'\r\nFirst = %s, Fill = %i" % (First, Fill) )
          # Just append and send the line back
         return (First + Last)
     
      # Figure out fill space required. Subtract 2 extra so we can add 2 spaces at the end
      fillSpace = " " * ( ( Fill - FirstLen ) - ( LastLen + 2 ) )
      return ( "%s%s%s%s" % (First, fillSpace, Last, "  ") )
       

   
   #==== Beginning of primary function ====

   if player.hp < ( ( float(player.maxhp) / 100) * 25 ):
      HealthStr = "horribly"
      hpcolor = amDefines.LRED
   elif player.hp < ( ( float(player.maxhp) / 100) * 50 ):
      HealthStr = "badly"
      hpcolor = amDefines.YELLOW
   elif player.hp < ( ( float(player.maxhp) / 100) * 75 ):
      HealthStr = "somewhat"
      hpcolor = amDefines.LGREEN
   elif player.hp < ( ( float(player.maxhp) / 100) * 85 ):
      HealthStr = "lightly"
      hpcolor = amDefines.WHITE
   elif player.hp < ( ( float(player.maxhp) / 100) * 95 ):
      HealthStr = "barely"
      hpcolor = amDefines.WHITE
   else:
      HealthStr = "not"
      hpcolor = amDefines.WHITE
      
   # If player.hp is higher than maxhp, make it blue (only a buff can do this)
   if player.hp > player.maxhp:
      hpcolor = amDefines.BLUE

      
   # Set fill length for FormatLineJustify and send the text to the user
   LFILL       = 30
   RFILL1      = 30
   RFILL2      = 27
   NumFill1    = 22
   NumFill2    = 52
   
   # Format the output strings for the stat output   
   Line1  = "%sName:%s %s" % ( amDefines.GREEN, amDefines.WHITE, player.name )
   
   L2a    = "%sRace:%s %s" % ( amDefines.GREEN, amDefines.WHITE, amRace.RaceList[player.race].name )
   L2b    = "%sClass:%s %s" % ( amDefines.GREEN, amDefines.WHITE, amRace.ClassList[player.Class].name )
   Line2  = FormatLineLJust(L2a, L2b, LFILL)
   
   L3a    = "%sHealth:%s" % ( amDefines.GREEN, amDefines.WHITE )
   L3b    = "%i of %i" % ( player.hp, player.maxhp )
   Line3  =  FormatLineRJust(L3a, L3b, RFILL1)
   
   # Line four
   L4a    = "%sOffense:%s" % ( amDefines.GREEN, amDefines.WHITE )
   L4b    = "%i" % ( player.offense )
   L4c    = "%sDefense:%s" % ( amDefines.GREEN, amDefines.WHITE )
   L4d    = "%i" % ( player.defense )
   Line4  = "%s%s" % ( FormatLineRJust(L4a, L4b, RFILL1), FormatLineRJust(L4c, L4d, RFILL2) )
   
   # Line 5
   L5a    = "%sSpellCasting:%s" % ( amDefines.GREEN, amDefines.WHITE )
   L5b    = "%i" % ( player.spellcasting )
   L5c    = "%sMagic Res:%s" % ( amDefines.GREEN, amDefines.WHITE )
   L5d    = "%i" % ( player.magicres )
   Line5  = "%s%s" % ( FormatLineRJust(L5a, L5b, RFILL1), FormatLineRJust(L5c, L5d, RFILL2) )
   
   Line6  = "%sStealth:%s %i" % ( amDefines.GREEN, amDefines.WHITE, player.stealth )
   
   Line7  = "%sYou are %s%s %s wounded." % ( amDefines.GREEN, hpcolor, HealthStr, amDefines.GREEN )
   
   Line8  = "%sYou have %i kills and %i deaths" % ( amDefines.GREEN, player.kills, player.deaths )
   
   # Separator line to make the stat look better and easier to read
   HR = "%s=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" % ( amDefines.WHITE )
   
   


   player.sendToPlayer( HR )
   player.sendToPlayer( Line1 )
   player.sendToPlayer( Line2 )
   player.sendToPlayer( Line3 )
   player.sendToPlayer( Line4 )
   player.sendToPlayer( Line5 )
   player.sendToPlayer( Line6 )   
   player.sendToPlayer( HR )   
   player.sendToPlayer( Line7 )
   player.sendToPlayer( Line8 )
    

   # Cycle through spells affecting the player and tell them
   for spell in player.Spells.values():
      if spell.statusText != "*":
         player.sendToPlayer(spell.statusText % (amDefines.BLUE, amDefines.WHITE) )
       
   # Tell the player about other status effecting the player
   if(player.resting):
      player.sendToPlayer("%sYou are resting." % (amDefines.BLUE))
   if(player.sneaking):
      player.sendToPlayer("%sYou are sneaking." % (amDefines.BLUE))
   if(player.isAdmin):
      player.sendToPlayer("%sYou have administrative privileges on the server." % (amDefines.YELLOW))
      
   return

#==================================================
# CastSpell()
#
# A spell command was given, try to cast it
#==================================================
def CastSpell( player, Cmd ):
   Spell = amSpells.SpellList[ Cmd[0] ]
   
   # IS this a skill or an actual spell?
   if Spell.stype == CASTING:
      ATTACKTYPE = CASTING
   elif Spell.stype == SKILL:
      ATTACKTYPE = SKILL

 
   # Can this player cast this spell? (spell and player are same class)
   if player.Class != Spell.Class:
      return False
   
   # If the caster hasn't cooled down from his last cast, he can't cast yet
   
   if player.SpellsCasted.has_key(Spell.SpellID):
      player.sendToPlayer("You can't do that right now!")
      return True
   
   # If spell is self only, no other arguments can be supplied.
   if len( Cmd ) > 1 and Spell.UsedOn == 1:
      player.sendToPlayer("%sYou cannot use this on others, only yourself!" % (amDefines.YELLOW))
      return True
   
   # If it must be casted on a victim enforce that here an argument must be supplied.
   if len( Cmd ) < 2 and Spell.UsedOn == 2:
      player.sendToPlayer("%sYou must specify a target!" % (amDefines.BROWN))
      return True

   # You can't cast and attack at the same time.
   if player.attacking == 1:
      player.factory.CombatQueue.RemoveAttack(player.playerid)
      player.attacking = 0
         
   # Just the command was given, can we cast it on ourself?
   if len( Cmd ) == 1 and ( Spell.UsedOn == 1 or Spell.UsedOn == 3 ):
      if amCombat.HitRoll( player, player, ATTACKTYPE ):
         Spell.ApplySpell( player, player )
         return True
      else:
         if Spell.failText != "*":
            failtext = Spell.failText.split("|")
            player.sendToPlayer(failtext[0] % (amDefines.WHITE, amDefines.WHITE) ) 
            player.sendToRoomNotVictim( player, failtext[1] % (amDefines.WHITE, player.name, amDefines.WHITE) )
         return True
      
   # A victim was given, is it castable on someone else?
   elif len (Cmd ) == 2 and Spell.UsedOn > 1:
      victimList = amUtils.FindPlayerInRoom(player, Cmd[1])

      # Anybody to attack?
      if len(victimList) == 0:
         player.sendToPlayer("You don't see %s here!" % (Cmd[1],))
         return True
      # Was more than one players name matching?
      elif len(victimList) > 1:
         player.sendToPlayer("Fix this, list all possible victims.")
         return True
      # Just one, attack!!!       
      else:
         victimID = victimList.keys()[0]          
         victim = player.factory.players[victimID]
         #if you cannot cast this on yourself, enforce that here
         if player == victim:
            player.sendToPlayer("%sYou cannot use this on yourself!" % (amDefines.YELLOW))
            return True
         else:
            if amCombat.HitRoll( player, victim, ATTACKTYPE ):
               Spell.ApplySpell( victim, player )
               return True
            else:
               if Spell.failText != "*":
                  failtext = Spell.failText.split("|")
                  player.sendToPlayer(failtext[0] % (amDefines.WHITE, amDefines.WHITE) )
                  player.sendToRoomNotVictim( player, failtext[1] % (amDefines.WHITE, player.name, amDefines.WHITE) )
               return True
                  
################################################
# Command -> ListSpells(player)
################################################
def ListSpells(player):
   
   player.sendToPlayer("%s<<=-=-=-=-=-=-=-=-=-=-= %sYour Spellbook%s =-=-=-=-=-=-=-=-=-=-=>>" % (amDefines.LCYAN, amDefines.LMAGENTA, amDefines.LCYAN))
   player.sendToPlayer("%s  Spell                Mnemonic     Cooldown     Duration" % (amDefines.GREEN))
      
   for Spell in amSpells.SpellList.values():
      if player.Class == Spell.Class:
         player.sendToPlayer("%s  %s %s %s %s" % (amDefines.LMAGENTA, Spell.name.ljust(20,' '), Spell.cmd.ljust(12,' '), str(Spell.CoolDown).rjust(8,' '), str(Spell.duration).rjust(8,' ')))
         
   player.sendToPlayer("%s<<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->>" % (amDefines.LCYAN))
         
   return

#################################################
# Command -> Reroll(player)
#################################################
def Reroll(player):

   # If player is playing, tell room player rerolled, and add a increment the players death count.
   if player.STATUS == amDefines.PLAYING:
      player.sendToRoom("%s%s decides to reroll, and disappears in a puff of smoke!" %(amDefines.YELLOW, player.name))
      player.deaths += 1

   amUtils.ResetPlayerStats(player)

   player.STATUS = amDefines.GETCLASS
   player.sendToPlayer("%s%s*** You have rerolled your character! ***\r\nPress enter to continue." % (amDefines.CLEARSCREEN, amDefines.BROWN))

   player.Rerolling = True
