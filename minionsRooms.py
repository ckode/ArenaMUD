import minionDefines

RoomList = {}

RoomActionID = { 1: "%s pushs the wall.|The wall slides out of the way!"
               }


class Room():
      def __init__(self):
         self.RoomNum          = 0
         self.Name             = ""
         self.Description      = ""
         self.LightLevel       = 1
         self.N                = 0
         self.NE               = 0
         self.E                = 0
         self.SE               = 0
         self.S                = 0
         self.SW               = 0
         self.W                = 0
         self.NW               = 0
         self.U                = 0
         self.D                = 0
         self.exits            = ""
         self.AltExits         = ""
         self.SecretPhrase     = ""
         self.ExitsToggle      = False
         self.SecretDirection  = 0
         self.SecretRoom       = 0
         self.ActionID         = 0
         self.ItemsInRoom      = {}
         self.ItemsInRoomCount = {}
         self.HiddenItems      = {}
         self.HiddenItemsCount = {}
         self.Players          = {}

      
      #Full room display
      def DisplayRoom(self, player):
          player.sendToPlayer(minionDefine.LCYAN + self.Name + "\n" + minionDefines.WHITE + self.Description)
          
      def GetPlayers(self):
          return self.Players



