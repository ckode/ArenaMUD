--  ArenaMUD - A multiplayer combat game - http://arenamud.david-c-brown.com
--  Copyright (C) 2009, 2010 - David C Brown & Mark Richardson
--
--  This program is free software: you can redistribute it and/or modify
--  it under the terms of the GNU General Public License as published by
--  the Free Software Foundation, either version 3 of the License, or
--  (at your option) any later version.
--
--  This program is distributed in the hope that it will be useful,
--  but WITHOUT ANY WARRANTY; without even the implied warranty of
--  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--  GNU General Public License for more details.
--
--  You should have received a copy of the GNU General Public License
--  along with this program.  If not, see <http://www.gnu.org/licenses/>.

-- Map Info
INSERT INTO "MapInfo" VALUES("Test Map", "A test map");

-- Rooms
INSERT INTO "rooms" VALUES(1,'Town Square','This is the Town Square of Dagnoroth!  You see trash piled up everywhere as ','the city has fallen from grace of the last few years! There appears to be ','a large hole here with a horrible smell rising from it.  To the north is the ','notorious Sonzo Ave.', "*", "1:1|5:5|3:7|7:9", 1, 0, 0, 1);
INSERT INTO "rooms" VALUES(2,'Northern Sonzo Ave','You are on Northern Sonzo Ave.  Sonzo Ave is the main thoroughfare and','it splits the city of Dagnoroth almost down the middle.  There are many','shops and other busineses located here.  There appears to be a green fog','that exist here. Sticking around to long is a bad idea. ','*', "1:2|5:1", 1, 0, 0, 0);
INSERT INTO "rooms" VALUES(3,'Northern Sonzo Ave','You are on Northern Sonzo Ave.  Sonzo Ave is the main thoroughfare and','it splits the city of Dagnoroth almost down the middle.  There are many','shops and other busineses located here.  There is a large underworld that','exists in Dagnoroth, though they usually avoid Sonzo Ave for the most part','due to the guard patrols that frequent here.', "1:3|5:2", 1, 0, 0, 0);
INSERT INTO "rooms" VALUES(4,'Northern Sonzo Ave','You are on Northern Sonzo Ave.  Sonzo Ave is the main thoroughfare and','it splits the city of Dagnoroth almost down the middle.  There are many','shops and other busineses located here.  There is a large underworld that','exists in Dagnoroth, though they usually avoid Sonzo Ave for the most part','due to the guard patrols that frequent here.', "1:4|5:3|3:6|7:6", 1, 0, 0, 0);
INSERT INTO "rooms" VALUES(5,'Northern Sonzo Ave','You are on Northern Sonzo Ave.  Sonzo Ave is the main thoroughfare and','it splits the city of Dagnoroth almost down the middle.  There are many','shops and other busineses located here.  There is a large underworld that','exists in Dagnoroth, though they usually avoid Sonzo Ave for the most part','due to the guard patrols that frequent here.', "1:5|5:4", 1, 0, 0, 0);

INSERT INTO "rooms" VALUES(6,'East Sloop Street','You are on .  Sloop St is the main thoroughfare and','it splits the city of Dagnoroth almost down the middle.  There are many','shops and other busineses located here.  There is a large underworld that','exists in Dagnoroth, though they usually avoid Sonzo Ave for the most part','due to the guard patrols that frequent here.', "3:8|7:7", 1, 0, 0, 0);
INSERT INTO "rooms" VALUES(7,'West Sloop Street','You are on Sloop St.  Sloop St is the main thoroughfare and','it splits the city of Dagnoroth almost down the middle.  There are many','shops and other busineses located here.  There is a large underworld that','exists in Dagnoroth, though they usually avoid Sonzo Ave for the most part','due to the guard patrols that frequent here.', "3:9|7:8", 1, 0, 0, 0);

-- Doors

INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (1, 1, 1, 2, 0, 0, 45, 1, 2);
INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (2, 1, 1, 2, 0, 0, 45, 2, 3);
INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (3, 1, 1, 2, 0, 0, 45, 3, 4);
INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (4, 1, 1, 2, 0, 0, 45, 4, 5);
INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (5, 4, 0, 1, 0, 0, 42, 5, 1);
INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (6, 4, 0, 1, 1, 1, 42, 4, 4);

INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (7, 1, 1, 2, 0, 0, 45, 1, 6);
INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (8, 1, 1, 2, 0, 0, 42, 6, 7);
INSERT INTO doors (id, DoorType, Passable, DoorStatus, DoesLock, Locked, DoorDesc, ExitRoom1, ExitRoom2) VALUES (9, 1, 1, 2, 0, 0, 42, 7, 1);

-- Room DOT Spells
INSERT INTO RoomSpells (id, hp_adjust, desc, name) VALUES (1, -4, "You feel sick.", "Poison Cloud");
INSERT INTO RoomSpells (id, hp_adjust, desc, name) VALUES (2, 4, "A light refreshing rain falls on you.", "Healing Rain");
INSERT INTO RoomSpells (id, hp_adjust, desc, name) VALUES (3, -10, "A volcanic explosion splashes you with lava!", "Volcano");
INSERT INTO RoomSpells (id, hp_adjust, desc, name) VALUES (4, -200, "You are crushed by a falling boulder!", "Falling Boulder");


-- Room Trap

-- stat: 1=hp (add more later)
INSERT INTO RoomTraps (id, stat, value, duration, playerdesc, roomdesc, name) VALUES (1, 1, -25, 0, "A trap springs and you are hit with a dart!", "%s springs a trap and writhes in pain!", "Dart Trap");

-- Items that spawn in rooms
INSERT INTO "Items" VALUES (3, 1);
INSERT INTO "Items" VALUES (10, 1);
