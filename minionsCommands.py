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
# Command Up
################################################
def Up(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[UP].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[UP].ToRoom
      # Remove user from old room
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.sendToRoom(minionDefines.WHITE + player.name + " just left up.")
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name + " just arrived from below.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[UP].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the up!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the up!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command Down
################################################
def Down(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[DOWN].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[DOWN].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left down.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from above.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[DOWN].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the down!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the down!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0

################################################
# Command North
################################################
def North(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[NORTH].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[NORTH].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the north.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the south.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[NORTH].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the north!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the north!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command NorthEast
################################################
def NorthEast(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[NE].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[NE].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the northeast.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the southwest.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[NE].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the northeast!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the northeast!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command East
################################################
def East(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[EAST].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[EAST].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the east.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the west.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[EAST].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the east!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the east!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0

################################################
# Command SouthEast
################################################
def SouthEast(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[SE].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[SE].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the southeast.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the northwest.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[SE].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the southeast!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the southeast!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0

################################################
# Command South
################################################
def South(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[SOUTH].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[SOUTH].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the south.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the north.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[SOUTH].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the south!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the south!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0

################################################
# Command SouthWest
################################################
def SouthWest(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[SW].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[SW].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the southwest.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the northeast.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[SW].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the southwest!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the southwest!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command West
################################################
def West(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[WEST].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[WEST].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the west.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the east.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[WEST].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the west!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the west!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command NorthWest
################################################
def NorthWest(player):
   global RoomList, BLOCKEDTEXT
   # Get new room ID
   if minionsRooms.RoomList[player.room].Doors[NW].Passable == True:
      NewRoom = minionsRooms.RoomList[player.room].Doors[NW].ToRoom
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the northwest.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the southeast.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      DoorType = minionsRooms.RoomList[player.room].Doors[NW].DoorType
      BLOCKED = minionsRooms.BLOCKEDTEXT[DoorType].split("|")
      player.sendToPlayer("%s%s%s%s" % (minionDefines.BLUE, BLOCKED[0], "to the northwest!", minionDefines.WHITE) )
      player.sendToRoom("%s%s%s%s%s" % (minionDefines.WHITE, player.name, BLOCKED[1], "to the northwest!", minionDefines.WHITE) )
      minionsUtils.StatLine(player)
   player.moving = 0


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

             player.sendToPlayer("%s%s%s" % (minionDefines.WHITE, "You open the ", minionsRooms.DOORTYPE[CurDoor.DoorType]) )
             player.sendToRoom("%s%s%s%s" % (minionDefines.WHITE, player.name, " opens the ", minionsRooms.DOORTYPE[CurDoor.DoorType]) )
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

          player.sendToPlayer("%s%s%s" % (minionDefines.WHITE, "You close the ", minionsRooms.DOORTYPE[CurDoor.DoorType]) )
          player.sendToRoom("%s%s%s%s" % (minionDefines.WHITE, player.name, " closes the ", minionsRooms.DOORTYPE[CurDoor.DoorType]) )
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


