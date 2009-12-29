import minionsRooms



#################################################
# WhoIsInThheRoom()
#
# Returns a dictionary of PlayerIDs mapped to
# Player's name from Room->Players dictionary
# of what players are in that room
#################################################
def WhoIsInTheRoom(player, RoomID):
   global RoomList

   PlayerList = {}

   _players = minionsRooms.RoomList[RoomID].Players.keys()
   for each in _players:
       PlayerList[each] = player.factory.players[each].name

   return PlayerList