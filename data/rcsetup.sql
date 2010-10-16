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


CREATE TABLE race (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(15) NOT NULL UNIQUE,
   description        INTEGER NOT NULL,         -- TextBlock ID
   BaseHP             INTEGER NOT NULL,
   DamageBonus        INTEGER NOT NULL,         -- Damage Bonus
   CastingBonus       INTEGER NOT NULL,         -- Casting bonus (better caster?)
   Vision             INTEGER NOT NULL,         -- 1 normal, 2 night, 3 DARK vision
   DefenseBonus       INTEGER NOT NULL,         -- Makes you harder to hit
   ToHitBonus         INTEGER NOT NULL,         -- Makes you more accurate
   Stealth            INTEGER NOT NULL          -- Bonus to stealth if class has stealth
);

CREATE TABLE class (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(15) NOT NULL UNIQUE,
   description        INTEGER NOT NULL,         -- TextBlock ID
   HPBonus            INTEGER NOT NULL,
   MinDamage          INTEGER NOT NULL,
   MaxDamage          INTEGER NOT NULL,
   BaseArmor          INTEGER NOT NULL,
   MageryType         INTEGER NOT NULL,
   Stealth            INTEGER NOT NULL,
   WeaponMessages     INTEGER NOT NULL
);