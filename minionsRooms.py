import minionDefines


class Room():
      RoomNum          = 0
      Name             = ""
      Description      = ""
      N                = 0
      NE               = 0
      E                = 0
      SE               = 0
      S                = 0
      SW               = 0
      W                = 0
      NW               = 0
      U                = 0
      D                = 0
      exits            = ""
      ItemsInRoom      = {}
      ItemsInRoomCount = {}
      HiddenItems      = {}
      HiddenItemsCount = {}
      Players          = []
      
      #Full room display
      def DisplayRoom(self, player):
          player.sendToPlayer(minionDefine.LCYAN + self.Name + "\n" + minionDefines.WHITE + self.Description)
      
      #def AddPlayerToRoom(playerID)
