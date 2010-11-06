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

import amLog, amDB, os


Map = None

class Arena:
    def __init__(self):
        self.name         = ""
        self.MapFile      = ""
        self.Rooms        = {}
        self.Doors        = {}
        self.RoomSpells   = {}
        self.RoomTraps    = {}


class ArenaQueue:
    def __init__(self):
        self.configFile      = "arenas.cfg"
        self.CurrentArena    = 0     # Current active map ID
        self.MaxArenas       = 0     # Total maps in rotation (be sure to subtract 1 after checking len() since indexes start at zero)
        self.ArenaNames      = {}    # List of maps names (not used yet)
        self.ArenaIndex      = {}    # Map ID->MapFileName
        self.arenaQueue      = []    # Queue to keep maps in correct order since Dicts are unordered
        self.ConfFileFail  = False

        # Load the arenas.cfg file
        self.ConfFileFail = self.GetArenaConfig()


    ####################################################
    # GetArenaConfig()
    #
    # 1. Load the map config
    # 2. Load each map and verify they are good (not yet implemented)
    # 3. Load map into index / queue and dump all maps and reload the first one
    ####################################################
    def GetArenaConfig(self):
        global Map
        
        if os.path.exists(self.configFile):
            try:
                fp = open(self.configFile, "r")
            except:
                ErrMesg = "Error: Could not open arenas.cfg"
                amLog.Logit(ErrMesg)
                self.ConfFileFail = True
                return True
        else:
            self.ConfFileFail = True
            ErrMesg = "Error: %s\arenas.cfg does not exist" % ( os.getcwd() )
            amLog.Logit(ErrMesg)
            return True
 

        x = 0
        for MapFile in fp.readlines():
            # Remove carrage returns from arena file names
            if MapFile[len(MapFile) - 1 :] == "\n":
                MapFile = MapFile[:-1]

            # Load and verify the map    
            CurMap = self.LoadArena( MapFile, Arena() )
            # If map is not bad, put it in the ArenaQueue      
            if CurMap != False:
                # Append maps to Index and Queue
                self.ArenaIndex[x] = MapFile
                self.arenaQueue.append(x)
                # If this is the first map, assign it to the global Map var
                if x == 0:
                    Map = CurMap
                x += 1
           
                
        self.MaxArenas = len(self.ArenaIndex) - 1
        fp.close()
        return False



    #################################################
    # LoadNextArena()
    #
    # Load the next Arena in the ArenaQueue
    #################################################
    def LoadNextArena(self):
        global Map
        
        # Check to see if this is the last arena in the queue.
        # If it is, reset CurrentArena to zero.
        if self.CurrentArena == self.MaxArenas:
            self.CurrentArena = 0
        # Else, increment CurrentArena
        else:
            self.CurrentArena += 1
        
        # Load next Arena.
        Map = self.LoadArena( self.ArenaIndex[self.CurrentArena], Arena() )
    
    #################################################
    # LoadArena()
    #
    # Load the map from the DB
    #################################################
    def LoadArena(self, MapFile, Arena):
        # Apply Path to filename
        Arena.MapFile = "%s\data\%s" % ( os.getcwd(), MapFile )

        if os.path.exists( Arena.MapFile ):
            # Load the doors
            try:
                Arena.Doors = amDB.LoadDoors( Arena.MapFile )
            except:
                ErrMesg = "Error: Failed to load doors from arena file: %s" % ( Arena.MapFile )
                amLog.Logit( ErrMesg )
                return False
    
            # Load the rooms
            try:
                Arena.Rooms = amDB.LoadRooms( Arena.MapFile )
            except:
                ErrMesg = "Error: Failed to load rooms from arena file: %s" % ( Arena.MapFile )
                amLog.Logit( ErrMesg )
                return False

            # Load the room spells
            try:
                Arena.RoomSpells = amDB.LoadRoomSpells( Arena.MapFile )
            except:
                ErrMesg = "Error: Failed to load rooms spells from arena file: %s" % ( Arena.MapFile )
                amLog.Logit( ErrMesg )
                return False
        
            # Load the rooms traps
            try:
                Arena.RoomTraps = amDB.LoadRoomTraps( Arena.MapFile )
            except:
                ErrMesg = "Error: Failed to load room traps from arena file: %s" % ( Arena.MapFile )
                amLog.Logit( ErrMesg )
                return False
        
            # Verify the map is consistent, else return False
            if self.VerifyArena( Arena ) == False:
                return False
        else:
            print "Map doesn't exist!"
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

        # Make sure all doors exist that rooms are point to.
        if self.VerifyDoorsExist(Arena) == False:
            amLog.Logit("Error: Room points to a door that does not exist in map: %s" % Arena.MapFile )

        # Make sure all rooms exist that doors point to.
        if self.VerifyRoomsExist(Arena) == False:
            amLog.Logit("Error: Door points to a room that does not exist in map: %s" % Arena.MapFile )
            return False
        
        # Make sure all room spells exist that rooms point to.
        if self.VerifyRoomSpellsExist(Arena) == False:
            amLog.Logit("Error: Rooms points to a room spell that does not exist in map: %s" % Arena.MapFile )
            return False
        
        # Make sure all room traps exist that rooms point to.
        if self.VerifyRoomTrapsExist(Arena) == False:
            amLog.Logit("Error: Rooms points to a room trap that does not exist in map: %s" % Arena.MapFile )
            return False
        
        # If here, arena has been verified.  Return true.
        return True

    ########################################################
    # VerifyDoorsExist()
    #
    # Make sure all doors exist that rooms are pointing to.
    ########################################################
    def VerifyDoorsExist(self, Arena):
        # Get list of Room IDs
        for Room in Arena.Rooms.values():
            # For each Room ID, get list of Doors IDs listed in the room.
            for DoorID in Room.Doors.values():
                # Check to see if the door ID exists in the Arena.Doors dict.
                if DoorID != 0 and Arena.Doors.has_key(DoorID):
                    continue
                else:
                    ErrMesg = "Door ID %i referenced in Arena %s by room ID %i, but door id does not exist." % ( DoorID, Arena.name, Room.RoonNum )
                    amLog.Logit( ErrMesg )
                    ErrMesg = "Skipping arena %s" % ( Arena.name )
                    amLog.Logit( ErrMesg )
                    return False
                    
            
        return True
    ########################################################
    # VerifyRoomsExist()
    #
    # Make sure all rooms exist that doors are pointing to.
    ########################################################
    def VerifyRoomsExist(self, Arena):
        for Door in Arena.Doors.values():
            for Room in Door.ExitRoom.values():
                if Room != 0 and Arena.Rooms.has_key(Room):
                    continue
                else:
                    ErrMesg = "Room ID %i referenced in Arena %s by door ID %i, but room id does not exist." % ( Room, Arena.name, Door.DoorNum )
                    amLog.Logit( ErrMesg )
                    ErrMesg = "Skipping arena %s" % ( Arena.name )
                    amLog.Logit( ErrMesg )
                    return False 
                
    ########################################################
    # VerifyRoomSpellsExist()
    #
    # Make sure all room spells exist that rooms are pointing to.
    ########################################################
    def VerifyRoomSpellsExist(self, Arena):
        for Room in Arena.Rooms.values():
            if Room.RoomSpell != 0:
                if Room.RoomSpell != 0 and Arena.RoomSpells.has_key(Room.RoomSpell):
                    continue
                else:
                    ErrMesg = "Room spell ID %i referenced in Arena %s by room ID %i, but room spell id does not exist." % ( Room.RoomSpell, Arena.name, Room.RoomNum )
                    amLog.Logit( ErrMesg )
                    ErrMesg = "Skipping arena %s" % ( Arena.name )
                    amLog.Logit( ErrMesg )
                    return False 
    
    ########################################################
    # VerifyRoomTrapsExist()
    #
    # Make sure all room traps exist that rooms are pointing to.
    ########################################################
    def VerifyRoomTrapsExist(self, Arena):
        for Room in Arena.Rooms.values():
            if Room.RoomTrap != 0: 
                if Arena.RoomTraps.has_key(Room.RoomTrap):
                    continue
                else:
                    ErrMesg = "Room trap ID %i referenced in Arena %s by room ID %i, but room trap id does not exist." % ( Room.RoomTrap, Arena.name, Room.RoomNum )
                    amLog.Logit( ErrMesg )
                    ErrMesg = "Skipping arena %s" % ( Arena.name )
                    amLog.Logit( ErrMesg )
                    return False 