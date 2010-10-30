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

import amLog

MapQueue      = {}


class MapQueue:
    def __init__(self):
        self.configFile    = "maps.cfg"
        self.CurrentMap    = 0     # Current active map ID
        self.MaxMaps       = 0     # Total maps in rotation (besure to subtract 1 after checking len() since indexes start at zero)
        self.MapNames      = {}    # List of maps names (not used yet)
        self.MapIndex      = {}    # Map ID->MapFileName
        self.mapQueue      = []    # Queue to keep maps in correct order since Dicts are unordered
        self.ConfFileFail  = False

        self.ConfFileFail = self.GetMapsConfig()


    ####################################################
    # GetMapsConfig()
    #
    # 1. Load the map config
    # 2. Load each map and verify they are good (not yet implemented)
    # 3. Load map into index / queue and dump all maps and reload the first one
    ####################################################
    def GetMapsConfig(self):
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
            # Remove carrage returns from map file names
            if each[len(each) - 1 :] == "\n":
                each = each[:-1]

            # Verify the map before appending it to the mapqueue
            if self.VerifyMap(each):
                # Append maps to Index and Queue
                self.MapIndex[x] = each
                self.mapQueue.append(x)
                x += 1


        fp.close()
        return False



    #################################################
    # LoadNextMap()
    #
    # Prepare everything for the next map like
    # resetting all stats, resetting player rooms,
    # figure out next map to be loaded, then call 
    # LoadMap() 
    #################################################
    def LoadNextMap(self):
        pass

    
    #################################################
    # LoadMap()
    #
    # Load the map from the DB
    #################################################
    def LoadMap(self, MapFile):
        pass


    #################################################
    # VerifyMap()
    #
    # Load a map and verify it loads and all doors,
    # rooms, traps, spells, and messages  are accounted
    # for that are specified within the map.
    #################################################
    def VerifyMap(self, MapFile):
        Rooms     = []
        Doors     = []
        Traps     = []
        Spells    = []

        Map = self.LoadMap(MapFile)

        # Make sure all doors exist that rooms are point to.
        if not self.VerifyDoorsExist(Map):
            amLog.Logit("Error: Room points to a door that does not exist in map: %s" % MapFile)

        # Make sure all rooms exist that doors point to.
        if not self.VerifyRoomsExist(Map):
            amLog.Logit("Error: Door points to a room that does not exist in map: %s" % MapFile)
            return False
        # Make sure all room spells exist that rooms point to.
        if not self.VerifyRoomSpellsExist(Map):
            amLog.Logit("Error: Rooms points to a room spell that does not exist in map: %s" % MapFile)
            return False
        # Make sure all room traps exist that rooms point to.
        if not self.VerifyRoomTrapsExist(Map):
            amLog.Logit("Error: Rooms points to a room trap that does not exist in map: %s" % MapFile)
            return False


    ########################################################
    # VerifyDoorsExist()
    #
    # Make sure all doors exist that rooms are pointing to.
    ########################################################
    def VerifyDoorsExist(Map):
        pass
    
    ########################################################
    # VerifyRoomsExist()
    #
    # Make sure all rooms exist that doors are pointing to.
    ########################################################
    def VerifyRoomsExist(Map):
        pass
    
    ########################################################
    # VerifyRoomSpellsExist()
    #
    # Make sure all room spells exist that rooms are pointing to.
    ########################################################
    def VerifyRoomSpellsExist(Map):
        pass
    
    ########################################################
    # VerifyRoomTrapsExist()
    #
    # Make sure all room traps exist that rooms are pointing to.
    ########################################################
    def VerifyRoomTrapsExist(Map):
        pass