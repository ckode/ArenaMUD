from twisted.internet import reactor

import minionDefines, minionsDB, minionsLog, minionsCommands
import minionsRooms, minionsUtils, minionsParser

import time

################################################
# Command Up
################################################
def Up(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].U
   if NewRoom != 0:
      # Remove user from old room
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.sendToRoom(minionDefines.WHITE + player.name + " just left up.")
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name + " just arrived from below.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.UP:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit up!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " tried to go through the ceiling, but failed!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command Down
################################################
def Down(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].D
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left down.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from above.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.DOWN:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit down!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the floor!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0

################################################
# Command North
################################################
def North(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].N
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the north.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the south.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.NORTH:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit north!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the wall to the north!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command NorthEast
################################################
def NorthEast(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].NE
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the northeast.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the southwest.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.NE:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit northeast!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the wall to the northeast!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command East
################################################
def East(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].E
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the east.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the west.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.EAST:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit east!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the wall to the east!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0

################################################
# Command SouthEast
################################################
def SouthEast(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].NE
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the southeast.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the northwest.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.SE:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit southeast!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the wall to the southeast!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0

################################################
# Command South
################################################
def South(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].S
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the south.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the north.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.SOUTH:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit south!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the wall to the south!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0

################################################
# Command SouthWest
################################################
def SouthWest(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].S
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the southwest.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the northeast.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.SW:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit southwest!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the wall to the southwest!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command West
################################################
def West(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].W
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the west.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the east.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.WEST:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit west!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the wall to the west!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command NorthWest
################################################
def NorthWest(player):
   global RoomList
   # Get new room ID
   NewRoom = minionsRooms.RoomList[player.room].NW
   if NewRoom != 0:
      # Remove user from old room
      player.sendToRoom(minionDefines.WHITE + player.name + " just left to the northwest.")
      del minionsRooms.RoomList[player.room].Players[player.playerid]
      player.room = NewRoom
      # Add player to that room
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.name
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from the southeast.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   elif minionsRooms.RoomList[player.room].ExitsToggle and minionsRooms.RoomList[player.room].SecretDirection == minionDefines.NW:
      NewRoom = minionsRooms.RoomList[player.room].SecretRoom
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
      player.sendLine(minionDefines.BLUE + "There is no exit northwest!" + minionDefines.WHITE)
      player.sendToRoom(minionDefines.WHITE + player.name + " ran into the wall to the northwest!" + minionDefines.WHITE)
      minionsUtils.StatLine(player)
   player.moving = 0


################################################
# Command -> QUIT
################################################
def Quit(player):
   player.disconnectClient()

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
    player.sendLine(minionDefines.GREEN + "You say: " + minionDefines.WHITE + line + minionDefines.WHITE)

################################################
# Command -> Emote
################################################
def Emote(player, line):
    player.sendToRoom(minionDefines.BLUE + player.name + " " + line)
    player.sendLine(minionDefines.BLUE + player.name + " " + line + minionDefines.WHITE)

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
    player.sendLine(minionDefines.GREEN + "You roll on the floor laughing!" + minionDefines.WHITE)
################################################
# Command -> Say
################################################
def Wtf(player):
    player.sendToRoom(minionDefines.GREEN + player.name + " yells, What the fuck!" + minionDefines.WHITE)
    player.sendLine(minionDefines.GREEN + "You yell, What the fuck!" + minionDefines.WHITE)

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
   player.sendLine(minionDefines.WHITE + Room.Description)
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

   if Room.ExitsToggle:
      player.sendLine(minionDefines.GREEN + "Obvious exits: " + Room.AltExits + minionDefines.WHITE)
   else:
      player.sendLine(minionDefines.GREEN + "Obvious exits: " + Room.exits + minionDefines.WHITE)
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


