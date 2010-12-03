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


CREATE TABLE rooms (
    id                INTEGER PRIMARY KEY,       -- Door ID
    name              VARCHAR(30) NOT NULL,
    desc1             VARCHAR(75) NOT NULL,      -- Room Long Description line 1
    desc2             VARCHAR(75) NOT NULL,      -- Room Long Description line 2
    desc3             VARCHAR(75) NOT NULL,      -- Room Long Description line 3
    desc4             VARCHAR(75) NOT NULL,      -- Room Long Description line 4
    desc5             VARCHAR(75) NOT NULL,      -- Room Long Description line 5
    doors             VARCHAR(75) NOT NULL,      -- List of door numbers split with |
    light             INTEGER NOT NULL,          -- Light Level (1 normal, 2 nightvision, 3 dark vision)
    roomspell         INTEGER NOT NULL,          -- spell that always casts in room
    trap              INTEGER NOT NULL,          -- trap that hits when someone enters the room
    nospawn           INTEGER NOT NULL           -- Zero you can spawn in this room, 1 you cannot
);

CREATE TABLE Doors (
    id                INTEGER PRIMARY KEY,       -- Door ID
    DoorType          INTEGER NOT NULL,          -- PATHWAY, Gate, S
    Passable          INTEGER NOT NULL,
    DoorStatus        INTEGER NOT NULL,          -- 1 open, 2 closed
    DoesLock          INTEGER NOT NULL,
    Locked            INTEGER NOT NULL,
    DoorDesc          INTEGER NOT NULL,
    ExitRoom1         INTEGER NOT NULL,
    ExitRoom2         INTEGER NOT NULL
);

CREATE TABLE RoomSpells (
    id                INTEGER PRIMARY KEY,
    hp_adjust         INTEGER NOT NULL,
    desc              VARCHAR(75) NOT NULL,
    name              VARCHAR(25) NOT NULL
);

CREATE TABLE RoomTraps (
    id                INTEGER PRIMARY KEY,
    stat              INTEGER NOT NULL,
    value             INTEGER NOT NULL,
    duration          INTEGER NOT NULL,
    playerdesc        VARCHAR(75) NOT NULL,
    roomdesc          VARCHAR(75) NOT NULL,
    name              VARCHAR(25) NOT NULL
);

CREATE TABLE MapInfo (
    name              VARCHAR(30) NOT NULL,
    description       VARCHAR(1024) NOT NULL
);


PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

INSERT INTO "MapInfo" VALUES("The Crypt", "A Crypt");

INSERT INTO "rooms" VALUES(1,'Crypt Entrance','This grim crypts facade is covered with hundreds of years of spider webs.','There appears to be very little light inside. Neglect has helped this once','beautiful entrance become a macabre ruin.','*','*','1:12|9:1',1,0,0,0);

INSERT INTO "rooms" VALUES(2,'Grassy field, above crypt','The grass sways gently with the breezes that flutter through this open','valley. Below, an irregular pit opens up to reveal a dark passage. ','You get the feeling that going in there is a mistake, but the lure of','riches may get the best of some who come across it.','*','3:3|7:2|10:1',1,0,0,0);

INSERT INTO "rooms" VALUES(3,'Grassy Plains','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','*','*','*','3:2|7:9',1,0,0,0);

INSERT INTO "rooms" VALUES(4,'Crypt hallway','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','1:13|5:12',1,0,0,0);

INSERT INTO "rooms" VALUES(5,'Crypt hallway','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','1:14|5:13',1,0,0,0);

INSERT INTO "rooms" VALUES(6,'Crypt hallway, intersection','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor. A couple of','hallways meet here.','*','1:23|3:15|5:14|7:19',1,0,0,0);

INSERT INTO "rooms" VALUES(7,'Crypt hallway','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','3:16|7:15',1,0,0,0);

INSERT INTO "rooms" VALUES(8,'Crypt hallway','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','5:17|7:16',1,0,0,0);

INSERT INTO "rooms" VALUES(9,'Crypt hallway','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','1:17|5:18',1,0,0,0);

INSERT INTO "rooms" VALUES(10,'Crypt hallway, dead end','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor. The hallway','comes to a sudden dead end here.','*','1:18',1,0,0,0);

INSERT INTO "rooms" VALUES(11,'Crypt hallway','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','3:19|7:20',1,0,0,0);

INSERT INTO "rooms" VALUES(12,'Crypt hallway','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','3:20|5:21',1,0,0,0);

INSERT INTO "rooms" VALUES(13,'Crypt hallway','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','1:21|5:22',1,0,0,0);

INSERT INTO "rooms" VALUES(14,'Crypt hallway, dead end','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor. The hallway','comes to a sudden dead end here.','*','1:22',1,0,0,0);

INSERT INTO "rooms" VALUES(15,'Deep crypt passage','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','1:24|5:23',1,0,0,0);

INSERT INTO "rooms" VALUES(16,'Deep crypt passage','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor.','*','*','1:25|5:24',1,0,0,0);

INSERT INTO "rooms" VALUES(17,'Deep crypt passage, end','This dank stone passage is covered with mildew. The footing is','extremely treacherous. The cool air condenses into swirling banks','of fog in places, while the denser fog churns near the floor. The passage','stops suddenly here and there is no light whatsoever.','*','5:25',1,0,1,0);

INSERT INTO "rooms" VALUES(18,'Grassy Plains','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','*','*','*','3:4|5:8|7:3',1,0,0,0);

INSERT INTO "rooms" VALUES(19,'Grassy Plains','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','*','*','*','4:5|7:4',1,0,0,0);

INSERT INTO "rooms" VALUES(20,'Grassy Plains','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','*','*','*','6:6|8:5',1,0,0,0);

INSERT INTO "rooms" VALUES(21,'Grassy Plains','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','*','*','*','2:6|8:7',1,0,0,0);

INSERT INTO "rooms" VALUES(22,'Grassy Plains','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','*','*','*','1:8|4:7',1,0,0,0);

INSERT INTO "rooms" VALUES(23,'Grassy Plains','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','*','*','*','3:9|7:10',1,0,0,0);

INSERT INTO "rooms" VALUES(24,'Grassy Plains','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','*','*','*','3:10|4:11',1,0,0,0);

INSERT INTO "rooms" VALUES(25,'Grassy Plains, dead end.','The grass sways gently with the breezes that flutter through this open','valley. The air here is pure and inspires a feeling of general well-being.','This circular opening seems like it should contain something, but rather','it is a dead end.','*','8:11',1,0,0,0);




INSERT INTO "Doors" VALUES(1,1,1,2,0,0,45,1,2);

INSERT INTO "Doors" VALUES(2,1,1,2,0,0,45,2,3);

INSERT INTO "Doors" VALUES(3,1,1,2,0,0,45,2,18);

INSERT INTO "Doors" VALUES(4,1,1,2,0,0,45,18,19);

INSERT INTO "Doors" VALUES(5,1,1,2,0,0,45,19,20);

INSERT INTO "Doors" VALUES(6,1,1,2,0,0,45,20,21);

INSERT INTO "Doors" VALUES(7,1,1,2,0,0,45,21,22);

INSERT INTO "Doors" VALUES(8,1,1,2,0,0,45,22,18);

INSERT INTO "Doors" VALUES(9,1,1,2,0,0,45,3,23);

INSERT INTO "Doors" VALUES(10,1,1,2,0,0,45,23,24);

INSERT INTO "Doors" VALUES(11,1,1,2,0,0,45,24,25);

INSERT INTO "Doors" VALUES(12,1,1,2,0,0,45,1,4);

INSERT INTO "Doors" VALUES(13,1,1,2,0,0,45,4,5);

INSERT INTO "Doors" VALUES(14,1,1,2,0,0,45,5,6);

INSERT INTO "Doors" VALUES(15,1,1,2,0,0,45,6,7);

INSERT INTO "Doors" VALUES(16,1,1,2,0,0,45,7,8);

INSERT INTO "Doors" VALUES(17,1,1,2,0,0,45,8,9);

INSERT INTO "Doors" VALUES(18,1,1,2,0,0,45,9,10);

INSERT INTO "Doors" VALUES(19,1,1,2,0,0,45,6,11);

INSERT INTO "Doors" VALUES(20,1,1,2,0,0,45,11,12);

INSERT INTO "Doors" VALUES(21,1,1,2,0,0,45,12,13);

INSERT INTO "Doors" VALUES(22,1,1,2,0,0,45,13,14);

INSERT INTO "Doors" VALUES(23,1,1,2,0,0,45,6,15);

INSERT INTO "Doors" VALUES(24,1,1,2,0,0,45,15,16);

INSERT INTO "Doors" VALUES(25,1,1,2,0,0,45,16,17);


INSERT INTO "RoomTraps" VALUES(1,1,-10,0,'A sharpened turd rockets out of a slit in the wall and lodges in your forehead!','A sharpened turd rockets out of a slit in the wall and lodges in forehead of %s!','Turd Darts');

COMMIT;
