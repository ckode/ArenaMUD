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


CREATE TABLE players (
    id                INTEGER PRIMARY KEY,
    name              VARCHAR(15) NOT NULL UNIQUE,
    lastname          VARCHAR(20) NOT NULL,
    passwd            VARCHAR(20) NOT NULL,
    hp                INTEGER NOT NULL,
    maxhp             INTEGER NOT NULL,
    mana              INTEGER NOT NULL,
    maxmana           INTEGER NOT NULL,
    mr                INTEGER NOT NULL,
    stealth           INTEGER NOT NULL,
    room              INTEGER NOT NULL
);

CREATE TABLE PlayerAttrs (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(30) NOT NULL,
   BriefDesc          VARCHAR(1024) NOT NULL    -- Brief explination of what this text block belongs too! (not used in game, only reference)
);