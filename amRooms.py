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

import amDefines, amUtils

RoomList          = {}
RoomSpellList     = {}
RoomTrapList      = {}
DoorList          = {}
AnsiScreen        = ''

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
        self.Desc1              = 0  # Full room discription
        self.Desc2              = 0  # Full room discription
        self.Desc3              = 0  # Full room discription
        self.Desc4              = 0  # Full room discription
        self.Desc5              = 0  # Full room discription
        self.NoSpawn            = 0  # Zero you can spawn here, 1 you cannot

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
        ObviousExits = "%sObvious exits: " % (amDefines.GREEN,)
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
                    DoorText = amUtils.MessageList[CurDoor.DoorDesc].split('|')[CurDoor.DoorStatus]

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



###############################################
# Door Object
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


class RoomSpell():
    def __init__(self):
        self.id                     = 0
        self.hp_adjust              = 0
        self.desc                   = ""


class RoomTrap():
    def __init__(self):
        self.id                     = 0
        self.stat                   = 0
        self.value                  = 0
        self.duration               = 0
        self.playerdesc             = ""
        self.roomdesc               = ""


