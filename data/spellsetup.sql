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


CREATE TABLE spells_items (
      id                INTEGER PRIMARY KEY,       -- Spell/Item ID
      name              VARCHAR(25) NOT NULL,      -- Item or spell name
      cmd               VARCHAR(4) NOT NULL,       -- Command used to evoke
      casted            INTEGER NOT NULL,          -- Is it picked up or casted (picked up 0, casted 1)
      cooldown          INTEGER NOT NULL,          -- How long after casting spell can you cast again
      use               INTEGER NOT NULL,          -- 1 self, 2 both, 3 other person, 4 area effect
      reqClass          INTEGER NOT NULL,          -- class IDs 
      duration          INTEGER NOT NULL,          -- How long it lasts 0 = instant like a single heal (if duration > 0 effects can go above max stat)
      durationEffect    INTEGER NOT NULL,          -- If an effect is applied each duration segment like damage, or healing.
      effects           VARCHAR(50) NOT NULL,      -- Stored as "stat: value" say HP = 1 "1: 20" would add 20HP
      guesture          VARCHAR(100) NOT NULL,     -- if item, %s picks up, if spell, makes guesture. separate self / room with "|" (or use "*" to ignore)
      effectText        VARCAHR(100) NOT NULL,     -- Text seen when duration effect happens. self only. (you feel better single heal, or You feel sick fo poison etc
      spellTextself     VARCHAR(100) NOT NULL,     -- Text displayed to self
      spellTextRoom     VARCHAR(100) NOT NULL,     -- Text displayed to room
      spellTextVictim   VARCHAR(100) NOT NULL,     -- Text displayed to person casted upon, set as "*" if self cast only or picked up item
      spellWearOff      VARCHAR(100) NOT NULL,     -- Wear off text if duration spell "*" if not
      statusText        VARCHAR(100) NOT NULL      -- The text shown to the player when he types status in the game that shows the spells effected by
);

