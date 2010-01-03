import minionDefines

RoomList = {}

RoomActionID = { 1: "%s pushs the wall.|The wall slides out of the way!"
               }

# Local defines for directions
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


NODOOR         = 0
PATHWAY        = 1
DOOR           = 2
SECRETDOOR     = 3




class Room():
      def __init__(self):
# Define Door Types

         self.RoomNum          = 0
         self.Name             = ""
         self.Desc1            = ""
         self.Desc2            = ""
         self.Desc3            = ""
         self.Desc4            = ""
         self.Desc5            = ""
         self.RoomType         = 0
         self.LightLevel       = 1
         self.SecretPhrase     = ""
         self.PhraseFunctionID = 0
         self.ActionID         = 0
         # Room doors/directions (holds Door class objects)   
         self.Doors            = { 1:    Door(), # North
                                   2:    Door(), # NE
                                   3:    Door(), # East
                                   4:    Door(), # SE
                                   5:    Door(), # South
                                   6:    Door(), # SW
                                   7:    Door(), # West
                                   8:    Door(), # NW
                                   9:    Door(), # Up
                                  10:    Door()  # Down
                                 }

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

      ##############################################################
      # DisplayExits()
      #
      # Return a string of the exits
      ##############################################################
      def DisplayExits(self):
          # If zero at the end, the return NONE!
          DoorCount = 0
          # Start string
          ObviousExits = "%sObvious exits: " % (minionDefines.GREEN,)
          EmptySize = len(ObviousExits)
          # North
          if self.Doors[NORTH].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(NORTH, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # Northeast
          if self.Doors[NE].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(NE, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1
          # East
          if self.Doors[EAST].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += GetDoorExit(EAST, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # Southeast
          if self.Doors[SE].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(SE, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # South
          if self.Doors[SOUTH].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(SOUTH, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # Southwest
          if self.Doors[SW].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(SW, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # West
          if self.Doors[WEST].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(WEST, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # Northwest
          if self.Doors[NW].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(NW, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # UP
          if self.Doors[UP].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(UP, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # Down
          if self.Doors[DOWN].DoorType != NODOOR:
             tmpSize = len(ObviousExits)
             ObviousExits += self.GetDoorExit(DOWN, DoorCount)
             if len(ObviousExits) > tmpSize:
                DoorCount += 1

          # Of no directions have been appended, append None, else append period.
          if len(ObviousExits) == EmptySize:
             ObviousExits += "None!"
          else:
             ObviousExits += "."
             return ObviousExits



      ############################################################################
      #  GetDoorExit()
      #
      # Return exit display to DisplayExits (this prevents duplicate code for each direction)
      ############################################################################
      def GetDoorExit(self, Direction, DoorCount):
            ObviousExits = ""
            STATUS = self.Doors[Direction].DoorStatus
            # If there is a Door visable, lets operate on it
            if STATUS != NONE:
               # Is there already a door in the list?  If so, append a comma for the next one
               if DoorCount > NONE:
                  ObviousExits += ", "
               ObviousExits += self.Doors[Direction].Exits[STATUS]
               return ObviousExits
            else:
               return ""





##############################################
class Door():

    def __init__(self):
        self.DoorType             = 0         # index of room type. ie. no door, path way (with no door), door, secret passage (hidden)
        self.DoorStatus           = 0         # Status of the exit. (0 = don't display, 1 = display open, 2 = display closed)
        self.Passable             = 0
        self.ToRoom               = 0         # Room number Door leads too
        self.DoorLocked           = 0         #(0 = not locked, 1 = locked)
        self.DoesLock             = 0         # Does the door lock?
        self.RequiredKey          = 0
        self.PickDiff             = 0
        self.Passable             = 0         # Can go through it. (0 no, 1 yes)
        self.Exits                = { 1: "", 2: "" }  # The display for Obvisous exits (1=open, 2=closed)



