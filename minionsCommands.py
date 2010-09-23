from twisted.internet import reactor

import minionDefines, minionsDB, minionsLog, minionsCommands
import minionsRooms, minionsUtils, minionsParser

import time, re


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


################################################
# NewMovePlayer() function
################################################
def MovePlayer(player, MoveText, Direction):
   global RoomList
   ActionText = MoveText.split("|")

   # Sub function that can be called when a player's path is blocked.
   def RunIntoWall(Action2, Action3, playerName):
      #DoorType = CurRoom.Doors[UP].DoorType
      player.sendToPlayer("%s%s%s" % (minionDefines.BLUE, Action2, minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s" % (minionDefines.WHITE, playerName, Action3, minionDefines.WHITE) )
      minionsUtils.StatLine(player)

   # Is the door in a passable state?
   if minionsRooms.RoomList[player.room].Doors.has_key(Direction):
      CurDoorNum = minionsRooms.RoomList[player.room].Doors[Direction]

      if minionsRooms.DoorList[CurDoorNum].Passable == True:
         # Get new room's room number, remove player from old room.
         NewRoom = minionsRooms.DoorList[CurDoorNum].ExitRoom[player.room]

         del minionsRooms.RoomList[player.room].Players[player.playerid]


         # Set players room num in his profile and tell room he left

         player.sendToRoom(minionDefines.WHITE + player.name + ActionText[0])
         player.room = NewRoom

         # Add player to that room and tell everyone
         minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
         player.sendToRoom(minionDefines.WHITE + player.name + ActionText[1])

         # Show the player the room he/she just entered
         minionsCommands.Look(player, player.room)
      else:
         RunIntoWall(ActionText[2], ActionText[3], player.name)
   else:
       RunIntoWall(ActionText[2], ActionText[3], player.name)

   player.moving = 0


################################################
# Command Up
################################################
def Up(player):
   global MessageList
   MovePlayer(player, minionsUtils.MessageList[9], UP)
   return

################################################
# Command Down
################################################
def Down(player):
   MovePlayer(player, minionsUtils.MessageList[10], DOWN)
   return

################################################
# Command North
################################################
def North(player):
   MovePlayer(player, minionsUtils.MessageList[1], NORTH)
   return

################################################
# Command NorthEast
################################################
def NorthEast(player):
   MovePlayer(player, minionsUtils.MessageList[2], NE)
   return

################################################
# Command East
################################################
def East(player):
   MovePlayer(player, minionsUtils.MessageList[3], EAST)
   return

################################################
# Command SouthEast
################################################
def SouthEast(player):
   MovePlayer(player, minionsUtils.MessageList[4], SE)
   return

################################################
# Command South
################################################
def South(player):
   MovePlayer(player, minionsUtils.MessageList[5], SOUTH)
   return
################################################
# Command SouthWest
################################################
def SouthWest(player):
   MovePlayer(player, minionsUtils.MessageList[6], SW)
   return

################################################
# Command West
################################################
def West(player):
   MovePlayer(player, minionsUtils.MessageList[7], WEST)
   return

################################################
# Command NorthWest
################################################
def NorthWest(player):
   MovePlayer(player, minionsUtils.MessageList[8], NW)
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
    obj = re.compile(re.escape(objList[0].lower()))
    # Only doors exist now
    if obj.match('north'):
       OpenDoor(player, NORTH)
       return
    elif obj.match('ne') and len(objList[0]) == 2 or obj.match('northeast') and len(objList[0]) > 5:
       OpenDoor(player, NE)
       return
    elif obj.match('east'):
       OpenDoor(player, EAST)
       return
    elif obj.match('se') and len(objList[0]) == 2 or obj.match('southeast') and len(objList[0]) > 5:
       OpenDoor(player, EAST)
       return
    elif obj.match('south'):
       OpenDoor(player, SOUTH)
       return
    elif obj.match('sw') and len(objList[0]) == 2 or obj.match('southwest') and len(objList[0]) > 5:
       OpenDoor(player, SW)
       return
    elif obj.match('west'):
       OpenDoor(player, WEST)
       return
    elif obj.match('nw') and len(objList[0]) == 2 or obj.match('northwest') and len(objList[0]) > 5:
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

    objList = something.split()[0]
    obj = re.compile(re.escape(objList[0].lower()))
    # Only doors exist now
    if obj.match('north'):
       CloseDoor(player, NORTH)
       return
    elif obj.match('ne') and len(objList[0]) == 2 or obj.match('northeast') and len(objList[0]) > 5:
       CloseDoor(player, NE)
       return
    elif obj.match('east'):
       CloseDoor(player, EAST)
       return
    elif obj.match('se') and len(objList[0]) == 2 or obj.match('southeast') and len(objList[0]) > 5:
       CloseDoor(player, EAST)
       return
    elif obj.match('south'):
       CloseDoor(player, SOUTH)
       return
    elif obj.match('sw') and len(objList[0]) == 2 or obj.match('southwest') and len(objList[0]) > 5:
       CloseDoor(player, SW)
       return
    elif obj.match('west'):
       CloseDoor(player, WEST)
       return
    elif obj.match('nw') and len(objList[0]) == 2 or obj.match('northwest') and len(objList[0]) > 5:
       CloseDoor(player, NW)
       return
    elif obj.match('up'):
       CloseDoor(player, UP)
       return
    elif obj.match('down'):
       CloseDoor(player, DOWN)
       return

################################################
# Command -> OpenDoor
################################################
def OpenDoor(player, DIRECTION):
    global RoomList, DIRTEXT
    CurDoor = minionsRooms.RoomList[player.room].Doors[DIRECTION]
    if CurDoor.Passable:
       player.sendToPlayer("%s%s is already open." % (minionDefines.WHITE, minionsRooms.DIRTEXT[DIRECTION].capitalize()) )
    else:
       # Is this a door and is it visable?
       if CurDoor.DoorType == 2 or CurDoor.DoorType == 4:
          # If locked, say so
          if CurDoor.DoorLocked == 1:
             player.sendToPlayer("%s%s%s" % (minionDefines.WHITE, CurDoor.Exits[1].capitalize(), " is locked.") )
          else:
             CurDoor.DoorType == 2 or CurDoor.DoorType == 4
             # Open the door on both sides of the door.
             minionsRooms.RoomList[player.room].Doors[DIRECTION].Passable = True
             minionsRooms.RoomList[player.room].Doors[DIRECTION].DoorStatus = minionsRooms.OPEN
             OtherRoom = minionsRooms.RoomList[player.room].Doors[DIRECTION].ToRoom
             if minionsRooms.RoomList[OtherRoom].Doors[minionsRooms.OPPOSITEDOOR[DIRECTION]].DoorType == CurDoor.DoorType:
                minionsRooms.RoomList[OtherRoom].Doors[minionsRooms.OPPOSITEDOOR[DIRECTION]].Passable = True
                minionsRooms.RoomList[OtherRoom].Doors[minionsRooms.OPPOSITEDOOR[DIRECTION]].DoorStatus = minionsRooms.OPEN
                player.BroadcastToRoom("%sThe %s to the %s opens." % (minionDefines.WHITE, minionsRooms.DOORTYPE[CurDoor.DoorType], minionsRooms.DIRTEXT[minionsRooms.OPPOSITEDOOR[DIRECTION]]), OtherRoom)

             player.sendToPlayer("%sYou open the %s to the %s" % (minionDefines.WHITE, minionsRooms.DOORTYPE[CurDoor.DoorType], minionsRooms.DIRTEXT[DIRECTION]) )
             player.sendToRoom("%s%s opens the %s to the %s" % (minionDefines.WHITE, player.name, minionsRooms.DOORTYPE[CurDoor.DoorType], minionsRooms.DIRTEXT[DIRECTION]) )
       else: # You don't see a door!
          player.sendToPlayer("%s%s%s" % (minionDefines.WHITE, "You do not see anything to open to the ", minionsRooms.DIRTEXT[DIRECTION]) )

################################################
# Command -> CloseDoor
################################################
def CloseDoor(player, DIRECTION):
    global RoomList, DIRTEXT
    CurDoor = minionsRooms.RoomList[player.room].Doors[DIRECTION]
    # Is this a door of type door or gate? (need to fix this so I just check 1 thing)
    if CurDoor.DoorType == 2 or CurDoor.DoorType == 4:
       if CurDoor.Passable == False:
          player.sendToPlayer("%s%s is already closed." % (minionDefines.WHITE, minionsRooms.DIRTEXT[DIRECTION].capitalize()) )
       else:
          minionsRooms.RoomList[player.room].Doors[DIRECTION].Passable = False
          minionsRooms.RoomList[player.room].Doors[DIRECTION].DoorStatus = minionsRooms.CLOSED
          OtherRoom = minionsRooms.RoomList[player.room].Doors[DIRECTION].ToRoom
          if minionsRooms.RoomList[OtherRoom].Doors[minionsRooms.OPPOSITEDOOR[DIRECTION]].DoorType == CurDoor.DoorType:
             minionsRooms.RoomList[OtherRoom].Doors[minionsRooms.OPPOSITEDOOR[DIRECTION]].Passable = False
             minionsRooms.RoomList[OtherRoom].Doors[minionsRooms.OPPOSITEDOOR[DIRECTION]].DoorStatus = minionsRooms.CLOSED
             player.BroadcastToRoom("%sThe %s to the %s closes." % (minionDefines.WHITE, minionsRooms.DOORTYPE[CurDoor.DoorType], minionsRooms.DIRTEXT[minionsRooms.OPPOSITEDOOR[DIRECTION]]), OtherRoom)

          player.sendToPlayer("%sYou close the %s to the %s" % (minionDefines.WHITE, minionsRooms.DOORTYPE[CurDoor.DoorType], minionsRooms.DIRTEXT[DIRECTION]) )
          player.sendToRoom("%s%s closes the %s to the %s" % (minionDefines.WHITE, player.name, minionsRooms.DOORTYPE[CurDoor.DoorType], minionsRooms.DIRTEXT[DIRECTION]) )
    else:
       player.sendToPlayer("%s%s%s" % (minionDefines.WHITE, "You do not see anything to close to the ", minionsRooms.DIRTEXT[DIRECTION]) )


################################################
# Command -> Gossip
################################################
def Gossip(player, line):
    #cmdLen = len(cmd[0]) + 1
    #player.Shout(minionDefines.MAGENTA + player.name + " gossips: " + line[cmdLen:] + minionDefines.WHITE )
    player.Shout(minionDefines.MAGENTA + player.name + " gossips: " + line)

################################################
# Command -> Who
################################################
def Who(player):
    player.sendToPlayer(minionDefines.LCYAN + "<<=-=-=-=-= Whos Online =-=-=-=>>")
    for user in player.factory.players.values():
        player.sendToPlayer(minionDefines.LCYAN + "  => " + minionDefines.LMAGENTA + user.name + " " + user.lastname)
    player.sendToPlayer(minionDefines.LCYAN + "<<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>>")
    minionsUtils.StatLine(player)

################################################
# Command -> Say
################################################
def Say(player, line):
    player.sendToRoom(minionDefines.GREEN + player.name + " says: " + minionDefines.WHITE + line)
    player.transport.write(minionDefines.DELETELEFT)
    player.transport.write(minionDefines.FIRSTCOL)
    player.sendToPlayer(minionDefines.GREEN + "You say: " + minionDefines.WHITE + line + minionDefines.WHITE)

################################################
# Command -> Emote
################################################
def Emote(player, line):
    player.sendToRoom(minionDefines.BLUE + player.name + " " + line)
    player.sendToPlayer(minionDefines.BLUE + player.name + " " + line + minionDefines.WHITE)

################################################
# Command -> Brief
################################################
def Brief(player):
    if player.briefDesc == 1:
       player.briefDesc = 0
       player.sendToPlayer(minionDefines.WHITE + "Verbose mode set.")
    else:
       player.briefDesc = 1
       player.sendToPlayer(minionDefines.WHITE + "Quiet mode set.")

################################################
# Command -> Help
################################################
def Help(player):
    width = 15
    for command in minionDefines.COMMANDS.keys():
        fill = width - (len(command) + 1)
        player.sendLine(minionDefines.MAGENTA + "   " + " " * fill + command + minionDefines.WHITE +  " => " +
                minionDefines.COMMAND_DEFS[minionDefines.COMMANDS[command]])

################################################
# Command -> Slap
################################################
def Slap(player, victim):
   global RoomList
   vict = {}
   if victim == "":
      player.sendToPlayer(minionDefines.BLUE + "You slap yourself!")
      player.sendToRoom(minionDefines.BLUE + player.name + " slaps himself!")
   else:
      vict = minionsUtils.FindPlayerInRoom(player, victim)
      if len(vict) == 0:
         return
      else:
         pid    = vict.keys()[0]
         name   = vict.values()[0]
         player.sendToPlayer(minionDefines.BLUE + "You slap " + name + "!")
         player.factory.players[pid].sendToPlayer(minionDefines.BLUE + player.name + " slaps you!")
         player.sendToRoomNotVictim(pid, minionDefines.BLUE + player.name + " slaps " + name + "!")

################################################
# Command -> Rofl
################################################
def Rofl(player):
    player.sendToRoom(minionDefines.GREEN + player.name + " rolls on the floor laughing!" + minionDefines.WHITE)
    player.sendToPlayer(minionDefines.GREEN + "You roll on the floor laughing!" + minionDefines.WHITE)
################################################
# Command -> Say
################################################
def Wtf(player):
    player.sendToRoom(minionDefines.GREEN + player.name + " yells, What the fuck!" + minionDefines.WHITE)
    player.sendToPlayer(minionDefines.GREEN + "You yell, What the fuck!" + minionDefines.WHITE)

################################################
# Command -> Look
################################################
def Look(player, RoomNum):
   global RoomList
   x = 1
   if RoomNum == "":
      RoomNum = player.room
   Room = minionsRooms.RoomList[RoomNum]
   if player.blind:
      player.sendLine(minionDefeines.WHITE + "You are blind!")
      minionsUtils.StatLine(player)
      return
   if player.vision < Room.LightLevel:
      if Room.LightLevel == minionDefines.DARKVISION:
         player.sendLine(minionDefines.WHITE + "The room is PITCH BLACK - you can't see anything!")
         minionsUtils.StatLine(player)
         return
      else:
         player.sendLine(minionDefines.WHITE + "The room is too dark, you can't see anything!")
         minionsUtils.StatLine(player)
         return
   player.sendLine(minionDefines.LCYAN + Room.Name)
   if player.briefDesc != 1:
      player.sendLine(minionDefines.WHITE + Room.Desc1)
      if Room.Desc2 != "*":
         player.sendLine(minionDefines.WHITE + Room.Desc2)
      if Room.Desc3 != "*":
         player.sendLine(minionDefines.WHITE + Room.Desc3)
      if Room.Desc4 != "*":
         player.sendLine(minionDefines.WHITE + Room.Desc4)
      if Room.Desc5 != "*":
         player.sendLine(minionDefines.WHITE + Room.Desc5)
   PeopleInRoom = minionsUtils.WhoIsInTheRoom(player, RoomNum)
   Count = len(PeopleInRoom)
   if Count > 1:
      names = minionDefines.GREEN + "Also here: " + minionDefines.LMAGENTA
      for each in PeopleInRoom.values():
         # You don't see yourself!
         if each != player.name:
            if (Count - 1) > x:
               x += 1
               names = names + each + ", "
            else:
               names = names + each + "." + minionDefines.WHITE

      player.sendLine(names)

   player.sendLine(Room.DisplayExits() + minionDefines.WHITE)
   minionsUtils.StatLine(player)
################################################
# Command -> Set <property>
################################################
def Set(player, line):
    parms = line.split()
    if len(parms) > 1:
       property = parms[0]
       value = parms[1]
    else:
       player.sendLine(minionDefines.DEFAULT + "Usage: SET <PROPERTY> <VALUE> - type 'help' for more help" + minionDefines.WHITE)
       return
    if property.lower() == "lastname":
       if len(value) > 20:
          player.sendLine(minionDefines.DEFAULT + "Lastnames limited to 20 characters, try again please." + minionDefines.WHITE)
          return
       player.lastname = value.capitalize()
       minionsDB.ChangeLastname(player.name, value)
       player.sendLine(minionDefines.DEFAULT + "Lastname updated." + minionDefines.WHITE)
    elif property.lower() == "password":
       if value == "":
          player.sendLine(minionDefines.DEFAULT + "Password cannot be blank." + minionDefines.WHITE)
          return
       if len(value) > 20:
          player.sendLine(minionDefines.DEFAULT + "Passwords limited to 20 characters, try again please." + minionDefines.WHITE)
          return
       player.password = value
       minionsDB.ChangePassword(player.name, value)
       player.sendLine(minionDefines.DEFAULT + "Password updated." + minionDefines.WHITE)
    else:
       player.sendLine(minionDefines.DEFAULT + "Usage: SET <PROPERTY> <VALUE> - type 'help' for more help" + minionDefines.WHITE)


