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


-- ============  Description of effect format ==================
-- Severeal stats and values can be listed as a spell may have more
-- than a single effect.
--
-- The format used is: "STAT:VALUE|STAT:VALUE|STAT:VALUE"
-- 
-- In an instances where a VALUE range exist for a stat, (like a healing range)
-- the value will be split by a % sign.  "STAT:VALUE_MIN%VALUE_MAX"
-- Healing spell example:   (1 = HP)
-- -- "1:10%25"
--
-- This example effect would heal HPs in a range of 10 to 25HPs. Negitive numbers
-- can be used for damage. Example: "1:-5%-25"
-- ==============================================================

-- Healing spell for Priest
INSERT INTO spell_items (
            1,            -- ID:              Spell / item ID
            "healing",    -- name:            Spell/Item Name as it appears in game
            "heal",       -- cmd:             Command used to cast it. (not used if ITEM)
            1,            -- casted:          1 = spell, 0 = item
            3,            -- Use:             For spells, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            4,            -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            0,            -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,            -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "1:10%25",    -- effects          * See below license info at top for explination
            "*",          -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "You feel better.",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "%sYou cast healing on yourself%s|%sNONE%s%s",
            -- spellTextRoom:  What the room not including you and the victim see
            "%s%s casts healing on %s%s",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "%s%s casts healing on you!%s",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "*"
);
 
            
            
            
            