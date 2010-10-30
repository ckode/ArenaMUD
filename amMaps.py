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

import amLog, amDB


class Arena:
    def __init__(self):
        self.Rooms        = []
        self.Doors        = []
        self.RoomSpells   = []
        self.RoomTraps    = []


class ArenaQueue:
    def __init__(self):
        self.configFile      = "maps.cfg"
        self.CurrentArena    = 0     # Current active map ID
        self.MaxArena        = 0     # Total maps in rotation (besure to subtract 1 after checking len() since indexes start at zero)
        self.ArenaNames      = {}    # List of maps names (not used yet)
        self.ArenaIndex      = {}    # Map ID->MapFileName
        self.arenaQueue      = []    # Queue to keep maps in correct order since Dicts are unordered
        self.ConfFileFail  = False

        self.ConfFileFail = self.GetArenaConfig()


    ####################################################
    # GetArenaConfig()
    #
    # 1. Load the map config
    # 2. Load each map and verify they are good (not yet implemented)
    # 3. Load map into index / queue and dump all maps and reload the first one
    ####################################################
    def GetArenaConfig(self):
        try:
            if os.path.exists(self.configFile):
                fp = open(self.configFile, "r")
            else:
                self.ConfFileFail = True
                ErrMesg = "Error: maps.cfg does not exist"
                amLog.Logit(ErrMesg)
                print ErrMesg
                return
        except:
            ErrMesg = "Error: Could not open maps.cfg"
            amLog.Logit(ErrMesg)
            print ErrMesg
            self.ConfFileFail = True
            return

        x = 0
        for each in fp.readlines():
            # Remove carrage returns from arena file names
            if each[len(each) - 1 :] == "\n":
                each = each[:-1]

            # Verify the arena before appending it to the mapqueue
            if self.VerifyArena(each):
                # Append maps to Index and Queue
                self.ArenaIndex[x] = each
                self.arenaQueue.append(x)
                x += 1


        fp.close()
        return False



    #################################################
    # LoadNextArena()
    #
    # Prepare everything for the next map like
    # resetting all stats, resetting player rooms,
    # figure out next map to be loaded, then call 
    # LoadMap() 
    #################################################
    def LoadNextArena(self):
        pass

    
    #################################################
    # LoadArena()
    #
    # Load the map from the DB
    #################################################
    def LoadArena(self, MapFile, Arena):
        # Load the doors
        try:
            Arena.Doors = amDB.NewLoadDoors( MapFile )
        except:
            ErrMesg = "Error: Failed to load doors in arena file: %s" % ( MapFile )
            amLog.Logit( ErrMesg )
            print ErrMesg
            return False
    
        # Load the rooms
        try:
            Arena.Rooms = amDB.NewLoadRooms( MapFile )
        except:
            ErrMesg = "Error: Failed to load rooms in arena file: %s" % ( MapFile )
            amLog.Logit( ErrMesg )
            print ErrMesg
            return False

        # Load the room spells
        try:
            Arena.RoomSpells = amDB.NewLoadRoomsSpells( MapFile )
        except:
            ErrMesg = "Error: Failed to load rooms spells in arena file: %s" % ( MapFile )
            amLog.Logit( ErrMesg )
            print ErrMesg
            return False
        
        # Load the rooms traps
        try:
            Arena.RoomTraps = amDB.NewLoadRoomTraps( MapFile )
        except:
            ErrMesg = "Error: Failed to load room traps in arena file: %s" % ( MapFile )
            amLog.Logit( ErrMesg )
            print ErrMesg
            return False
        
        # Verify the map is consistent, else return False
        if self.VerifyArena( Arena ) == False:
            return False
        
        # Arena is loaded and check for consistency, return the Arena (map)
        return Arena
        
    #################################################
    # VerifyArena()
    #
    # Load a map and verify it loads and all doors,
    # rooms, traps, spells, and messages  are accounted
    # for that are specified within the map.
    #################################################
    def VerifyArena(self, Arena):      
        Rooms     = []
        Doors     = []
        Traps     = []
        Spells    = []
        
        # Remove this return later
        if 1:
            return True

        # Make sure all doors exist that rooms are point to.
        if self.VerifyDoorsExist(Arena) == False:
            amLog.Logit("Error: Room points to a door that does not exist in map: %s" % MapFile)

        # Make sure all rooms exist that doors point to.
        if self.VerifyRoomsExist(Arena) == False:
            amLog.Logit("Error: Door points to a room that does not exist in map: %s" % MapFile)
            return False
        # Make sure all room spells exist that rooms point to.
        if self.VerifyRoomSpellsExist(Arena) == False:
            amLog.Logit("Error: Rooms points to a room spell that does not exist in map: %s" % MapFile)
            return False
        # Make sure all room traps exist that rooms point to.
        if self.VerifyRoomTrapsExist(Arena) == False:
            amLog.Logit("Error: Rooms points to a room trap that does not exist in map: %s" % MapFile)
            return False
        
        return True

    ########################################################
    # VerifyDoorsExist()
    #
    # Make sure all doors exist that rooms are pointing to.
    ########################################################
    def VerifyDoorsExist(self, Arena):
        pass
    
    ########################################################
    # VerifyRoomsExist()
    #
    # Make sure all rooms exist that doors are pointing to.
    ########################################################
    def VerifyRoomsExist(self, Arena):
        pass
    
    ########################################################
    # VerifyRoomSpellsExist()
    #
    # Make sure all room spells exist that rooms are pointing to.
    ########################################################
    def VerifyRoomSpellsExist(self, Arena):
        pass
    
    ########################################################
    # VerifyRoomTrapsExist()
    #
    # Make sure all room traps exist that rooms are pointing to.
    ########################################################
    def VerifyRoomTrapsExist(self, Arena):
        pass