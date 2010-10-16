--  ArenaMUD - A multiplayer combat game - http://arenamud.david-c-brown.com
--  Copyright (C) 2010 - David C Brown & Mark Richardson
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


-- MessageTypes:
-- 1 Weapon messages
-- 2 Door open/close messages

-- Door Types

INSERT INTO messages (id, message, BriefDesc, MessageType) values (41,  "door|closed door|open door", "message for door and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (42,  "gate|closed gate|open gate", "message for gate and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (43,  "trap door|open trap door", "message for trap door and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (44,  "wall|wall|open secret passage", "message for secret passage and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (45,  "wall|BLANK|BLANK", "Just an passage, no messages", 2);


-- Weapon Messages
INSERT INTO messages (id, message, BriefDesc, MessageType) values (1, "%sYou swing your axe at %s, but miss!%s|%sYou chop %s for %i damage!%s|%sYou surprise chop %s for %i damage!%s|%s%s swings at you with an axe, but misses!|%s%s chops you for %i damage!%s|%s%s surprise chops you for %i damage!%s|%s%s swings at %s, but misses!|%s%s chops %s for %i damage!%s|%s%s surprise chops %s for %i damage!%s", "Weapon messages for Barbarian", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (2, "%sYou try to fire a magic missle at %s, but failed!%s|%sYou fire a magic missle at %s for %i damage!%s|NONE|%s%s tries to fire a magic missle at you, but fails!%s|%s%s fires a magic missle at you for %i damage!%s|NONE|%s%s tries to fire a magic missle at %s, but failed!%s|%s%s fires a magic missle at %s for %i damage!%s|NONE", "Weapon messages for mage", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (3, "%sYou swing your shortsword at %s, but miss!%s|%sYou slice %s for %i damage!%s|%sYou surprise slice %s for %i damage!%s|%s%s swings at you with a shortsword, but misses!%s|%s%s slices you for %i damage!%s|%s%s surprise slices you for %i damage!%s|%s swings at %s, but misses!%s|%s%s slices %s for %i damage!%s|%s%s surprise slices %s for %i damage!%s", "Weapon messages for thief", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (4, "%sYou tries to cast holy force at %s, but failed!%s|%sYou blasts %s with holy force for %i damage!%s|NONE|%s%s tries to cast holy force at you, but failed!%s|%s%s blasts you with holy force for %i damage!%s|NONE|%s%s tries to cast holy force at %s, but failed!%s|%s%s blasts %s with holy force for %i damage!%s|NONE", "Weapon messages for priest", 1);