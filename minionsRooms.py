import minionDefines, minionsUtils

RoomList = {}
DoorList = {}

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
GATE           = 4

# Door Status
HIDDEN         = 0
OPEN           = 2
CLOSED         = 1

# Text displayed when your path is blocked
# Should match Door Types listed above
BLOCKEDTEXT    = { 0: "You run into the wall | runs into the wall ",
                   1: " | ",
                   2: "You run into the door | runs into the door ",
                   3: "You run into the wall | runs into the wall ",
                   4: "You run into the gate | runs into the gate "
                 }

# Door type names
DOORTYPE       = {
                   2: "door",
                   4: "gate"
                 }
OPPOSITEDOOR   =  { NORTH: SOUTH,
                    NE: SW,
                    EAST: WEST,
                    SE: NW,
                    SOUTH: NORTH,
                    SW: NE,
                    WEST: EAST,
                    NW: SE,
                    UP: DOWN,
                    DOWN: UP
                 }
DIRTEXT        = { 1: 'north',
                   2: 'northeast',
                   3: 'east',
                   4: 'southeast',
                   5: 'south',
                   6: 'southwest',
                   7: 'west',
                   8: 'northwest',
                   9: 'up',
                  10: 'down'
                 }

DIRLOOKUP      = { "n":    1,
                   "ne":   2,
                   "e":    3,
                   "se":   4,
                   "s":    5,
                   "sw":   6,
                   "w":    7,
                   "nw":   8,
                   "u":    9,
                   "d":   10
                 }

#################################
# New room Object
#################################
class RoomObj():
    def __init__(self):
        self.RoomNum           = 0   # Room ID
        self.Name              = ""  # Title of the room
        self.Desc1              = 0   # Full room discription
        self.Desc2              = 0   # Full room discription
        self.Desc3              = 0   # Full room discription
        self.Desc4              = 0   # Full room discription
        self.Desc5              = 0   # Full room discription

        self.Doors             = {}  # Doors{direction: DoorID}
        self.LightLevel        = 0   # Light level in room
        self.RoomSpell         = 0   # The ID of a spell that continuously casts in the room.
        self.PlayerTrap        = 0   # Trap set by player, only lands once then is gone.
        self.RoomTrap          = 0   # Room trap, hits everytime you enter room

        self.ItemsInRoom       = {}  # Items laying on the ground in the room
        self.ItemsInRoomCount  = {}  # Count of how many items are on the ground (do we need this?)
        self.Players           = {}  # List of players currently in the room


    ##########################
    # FIX THIS FOR MessageList reading for door text (open door)
    #########################
    def DisplayExits(self):
          DoorCount = 0
          # Start string
          ObviousExits = "%sObvious exits: " % (minionDefines.GREEN,)
          EmptySize = len(ObviousExits)

          # Cycle through the doors in the room and build the obvious exits string
          for _door in self.Doors.keys():
              _door = int(_door)

              # Make current door local var to shorten the var mapping code
              CurDoor = DoorList[self.Doors[_door]]

              # If the door is NOT invisable, this go ahead.
              if CurDoor.DoorStatus != 0:

                  DoorCount = DoorCount + 1
                  # Is it only a pathway and not a door that requires more of a discription?
                  if CurDoor.DoorType == PATHWAY:
                      # Just display direction (east)
                      if DoorCount > 1:
                          ObviousExits += ", " + DIRTEXT[_door]
                      else:
                          ObviousExits += DIRTEXT[_door]
                  # Display door type, status, and direction (door open east)
                  else:
                      DoorText = minionsUtils.MessageList[CurDoor.DoorDesc].split('|')[CurDoor.DoorStatus]

                      if DoorCount > 1:
                          ObviousExits += ", " + DoorText + " " + DIRTEXT[_door]
                      else:
                          ObviousExits += DoorText + " " + DIRTEXT[_door]


          # Return NONE, or add the finally period to close the sentence
          if DoorCount == 0:
              ObviousExits += "NONE!"
          else:
              ObviousExits += "."

          return ObviousExits

    ###########################################
    # Return the Door ID for said direction
    ###########################################
    def GetDoorID(self, Direction):
        if self.Doors.has_key(Direction):
            return self.Doors[Direction]
        # No door, return zero
        return 0



################################################################
# Not currently in use
################################################################
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
             ObviousExits += self.GetDoorExit(EAST, DoorCount)
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



###############################################
# New Door Object to replace old door object
# *** Not currently in use ***
###############################################
class DoorObj():
    def __init__(self):
        self.DoorNum              = 0         # Door ID
        self.DoorType             = 0         # TextBlock lookup for door description (pathway, door, secret passage, gate)
        self.DoorStatus           = 0         # Status of the exit. (0 = don't display, 1 = display open, 2 = display closed)
        self.Passable             = 0         # Can pass through door
        self.DoesLock             = 0         # lockable?
        self.Locked               = 0         # Is it currently locked?
        self.DoorDesc             = 0         # DoorDesc[DoorStatus] returns description ID from Description lookup table
        self.ExitRoom             = {}        # ExitRoom[CurrentRoom] returns room number of the exit room

    ##################################################
    # Get the Room ID on the other side of the door
    ##################################################
    def GetOppositeRoomID(self, CurRoom):

        if self.ExitRoom[CurRoom] > 0:
            return self.ExitRoom[CurRoom]

        # If zero, return zero
        return 0
##############################################
# ResetDoor()
#
# This needs lots of work for closing and locking
# doors, telling the rooms they closed and locked
# No call to this implemented yet
#
# Resets the door to it's default status
# Locked, hidden, etc based on DoorType
##############################################
    def ResetDoor(self):
        if self.DoorType == SECRETDOOR:
           self.DoorStatus = HIDDEN
           self.Passable = False
        else:
           self.DoorStatus = CLOSED
           self.Passable = False

