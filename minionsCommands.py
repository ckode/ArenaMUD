from twisted.internet import reactor

import minionDefines, minionsDB, minionsLog, minionsCommands
import minionsRooms, minionsUtils

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
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.playerid
      player.sendToRoom(minionDefines.WHITE + player.name + " just arrived from below.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      player.sendLine(minionDefines.BLUE + "There is no exit up!" + minionDefines.WHITE)


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
      minionsRooms.RoomList[NewRoom].Players[player.playerid] = player.playerid
      player.sendToRoom(minionDefines.WHITE + player.name +" just arrived from above.")
      # Show the player the room he/she just entered
      minionsCommands.Look(player, player.room)
   else:
      player.sendLine(minionDefines.BLUE + "There is no exit down!" + minionDefines.WHITE)


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

   player.sendLine(minionDefines.GREEN + "Obvious exits: " + Room.exits + minionDefines.WHITE)
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


