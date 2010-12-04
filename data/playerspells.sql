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
INSERT INTO spells_items VALUES (
            1,            -- ID:              Spell / item ID
            "healing",    -- name:            Spell/Item Name as it appears in game
            "heal",       -- cmd:             Command used to cast it. (not used if ITEM)
            1,            -- casted:          1 = spell, 0 = item
            8,            -- cooldown         How long it takes to cool down to cast again
            3,            -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            4,            -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            0,            -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,            -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "1:10%25",    -- effects          * See below license info at top for explination
            -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            "*",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "%sYou feel better.%s",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "%sYou cast healing on %s%s",
            -- spellTextRoom:  What the room not including you and the victim see
            "%s%s casts healing on %s%s",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "%s%s casts healing on you!%s",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "*",
            -- statusText:    Spell Status Text (when typing stats
            "*"
);
 

-- Druid Doom spell
INSERT INTO spells_items VALUES (
            2,            -- ID:              Spell / item ID
            "creeping doom",    -- name:            Spell/Item Name as it appears in game
            "doom",       -- cmd:             Command used to cast it. (not used if ITEM)
            1,            -- casted:          1 = spell, 0 = item
            30,           -- cooldown         How long it takes to cool down to cast again
            2,            -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            5,            -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            15,           -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            1,            -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "1:-3",       -- effects          * See below license info at top for explination
            -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            "%sYou reach for the sky!%s|%s%s reaches for the sky.%s",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "%sThe swarm is biting you!%s",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "%sYou cast creeping doom on %s!%s",
            -- spellTextRoom:  What the room not including you and the victim see
            "%s%s casts creeping doom on %s%s",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "%s%s casts creeping doom on you!%s",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sThe swarm has left.%s",
            -- statusText:    Spell Status Text (when typing stats
            "%sYou are being attacked by a swarm of insects!%s"
);
            

-- Healing potion 
INSERT INTO spells_items VALUES (
            3,                    -- ID:              Spell / item ID
            "healing potion",        -- name:            Spell/Item Name as it appears in game
            "*",                  -- cmd:             Command used to cast it. (not used if ITEM)
            0,                    -- casted:          1 = spell, 0 = item
            30,                   -- cooldown         How long it takes to cool down to cast again (respawn for items)
            0,                    -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            0,                    -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            0,                    -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,                    -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "1:15%30",             -- effects          * See below license info at top for explination
            -- gesture     Use "*" for none, this is any pre-cast gestures made. 
            "%sYou pick up a healing potion and drink it!%s|%s%s picks up a healing potion and drinks it!%s",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "%sYou feel better.%s",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "*",
            -- spellTextRoom:  What the room not including you and the victim see
            "*",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "*",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "*",
            -- statusText:    Spell Status Text (when typing stats
            "*"
);
       
-- Entangle spell for Druids
INSERT INTO spells_items VALUES (
            4,            -- ID:              Spell / item ID
            "entangle",   -- name:            Spell/Item Name as it appears in game
            "enta",       -- cmd:             Command used to cast it. (not used if ITEM)
            1,            -- casted:          1 = spell, 0 = item
            12,           -- cooldown         How long it takes to cool down to cast again
            2,            -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            5,            -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            5,            -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,            -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "10:1",       -- effects          * See below license info at top for explination
            -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            "%sYou point at the ground!%s|%s%s points at the ground!%s",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "*",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "%sYou cast entangle on %s%s",
            -- spellTextRoom:  What the room not including you and the victim see
            "%s%s casts entangle on %s%s",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "%s%s casts entangle on you!%s",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sYou are freed!%s",
            -- statusText:    Spell Status Text (when typing stats
            "%sYou have been entangled by surrounding plants!%s"
);


-- Hold Person spell for Priest
INSERT INTO spells_items VALUES (
            5,               -- ID:              Spell / item ID
            "hold person",   -- name:            Spell/Item Name as it appears in game
            "hold",          -- cmd:             Command used to cast it. (not used if ITEM)
            1,               -- casted:          1 = spell, 0 = item
            12,              -- cooldown         How long it takes to cool down to cast again
            2,               -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            4,               -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            5,               -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,               -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "10:1",          -- effects          * See below license info at top for explination
            -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            "*",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "*",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "%sYou cast hold person on %s%s",
            -- spellTextRoom:  What the room not including you and the victim see
            "%s%s casts hold person on %s%s",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "%s%s casts hold person on you!%s",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sYou are no longer held!%s",
            -- statusText:    Spell Status Text (when typing stats
            "%sYou are being held by some unseen force!%s"
);


-- Slam for barb
INSERT INTO spells_items VALUES (
            6,            -- ID:              Spell / item ID
            "slam",       -- name:            Spell/Item Name as it appears in game
            "slam",       -- cmd:             Command used to cast it. (not used if ITEM)
            1,            -- casted:          1 = spell, 0 = item
            15,           -- cooldown         How long it takes to cool down to cast again
            2,            -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            1,            -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            2,            -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,            -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "1:-15|11:1",  -- effects          * See below license info at top for explination
            -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            "*",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "*",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "%sYou slam %s to the ground!%s",
            -- spellTextRoom:  What the room not including you and the victim see
            "%s%s slams %s to the ground!%s",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "%s%s slams you to the ground!%s",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sYou get up and rub some dirt on it.%s",
            -- statusText:    Spell Status Text (when typing stats
            "*"
);

-- Blade Poison for Thief
INSERT INTO spells_items VALUES (
            7,            -- ID:              Spell / item ID
            "thieves poison",   -- name:      Spell/Item Name as it appears in game
            "pois",       -- cmd:             Command used to cast it. (not used if ITEM)
            1,            -- casted:          1 = spell, 0 = item
            60,           -- cooldown         How long it takes to cool down to cast again
            1,            -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            3,            -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            15,           -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,            -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "12:-3",      -- effects          * See below license info at top for explination
            -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            "%sYou apply poison to your sword!%s|%s%s applies poison to their sword!%s",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "%sYou feel sick.%s",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "*",
            -- spellTextRoom:  What the room not including you and the victim see
            "*",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "*",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sYour blade is no longer poisoned.%s",
            -- statusText:    Spell Status Text (when typing stats
            "*"
);


-- Weakness for Mages
INSERT INTO spells_items VALUES (
            8,            -- ID:              Spell / item ID
            "weakness",   -- name:      Spell/Item Name as it appears in game
            "weak",       -- cmd:             Command used to cast it. (not used if ITEM)
            1,            -- casted:          1 = spell, 0 = item
            60,           -- cooldown         How long it takes to cool down to cast again
            2,            -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            2,            -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            15,           -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,            -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "3:-5|4:-5|6:-10|7:-5",      -- effects          * See below license info at top for explination
            -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            "*",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "*",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "%sYou cast weakness on %s!%s",
            -- spellTextRoom:  What the room not including you and the victim see
            "%s%s casts weakness on %s!%s",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "%s%s casts weakness on you!%s",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sYou feel stronger.%s",
            -- statusText:    Spell Status Text (when typing stats
            "%sYou feel weak!%s"
);


-- Slam for barb
INSERT INTO spells_items VALUES (
            9,            -- ID:              Spell / item ID
            "cone of ice",    -- name:        Spell/Item Name as it appears in game
            "cone",       -- cmd:             Command used to cast it. (not used if ITEM)
            1,            -- casted:          1 = spell, 0 = item
            25,           -- cooldown         How long it takes to cool down to cast again
            2,            -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            2,            -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            2,            -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,            -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "11:1",       -- effects          * See below license info at top for explination
            -- gesture          Use "*" for none, this is any pre-cast gestures made. 
            "*",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "*",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "%sYou you cast cone of ice on %s!%s",
            -- spellTextRoom:  What the room not including you and the victim see
            "%s%s casts cone of ice on %s!%s",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "%s%s casts cone of ice on you!%s",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sYou thaw out.%s",
            -- statusText:    Spell Status Text (when typing stats
            "%sYou are frozen!%s"
);


-- ring of natural healing
INSERT INTO spells_items VALUES (
            10,                   -- ID:              Spell / item ID
            "ring of natural healing",   -- name:            Spell/Item Name as it appears in game
            "*",                  -- cmd:             Command used to cast it. (not used if ITEM)
            0,                    -- casted:          1 = spell, 0 = item
            180,                  -- cooldown         How long it takes to cool down to cast again (respawn for items)
            0,                    -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            0,                    -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            60,                   -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            0,                    -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "9:10",               -- effects          * See below license info at top for explination
            -- gesture     Use "*" for none, this is any pre-cast gestures made. 
            "%sYou pick up the ring of natural healing and wear it.%s|%s%s picks up the ring of natural healing and wears it!%s",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "*",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "*",
            -- spellTextRoom:  What the room not including you and the victim see
            "*",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "*",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sThe ring of natural healing vanishes!%s",
            -- statusText:    Spell Status Text (when typing stats
            "%sYou are wearing a ring of natural healing.%s"
);

-- glowing vial
INSERT INTO spells_items VALUES (
            11,                   -- ID:              Spell / item ID
            "glowing vial",   -- name:            Spell/Item Name as it appears in game
            "*",                  -- cmd:             Command used to cast it. (not used if ITEM)
            0,                    -- casted:          1 = spell, 0 = item
            180,                  -- cooldown         How long it takes to cool down to cast again (respawn for items)
            0,                    -- Use:             For spells, 0 = item, 1 = cast on self, 2, cast on victim, 3 = Cast on anyone, 4 = AreaEffect
            0,                    -- reqClass:        Class required to cast. 0 for items / ALL (4 = priest)
            15,                   -- duration         How long a spell lasts. 0 Instant, duration loop = 2 seconds, 30sec spell = 15 duration
            1,                    -- durationEffect   Does a effect happen each duration loop (damage/healing ever 2 seconds, etc) stat boost = 0 durEff
            "1:5",                -- effects          * See below license info at top for explination
            -- gesture     Use "*" for none, this is any pre-cast gestures made. 
            "%sYou pick up the glowing vial and quaff it.%s|%s%s picks up the glowing vial and quaffs it!%s",          
            -- Text effect:    The effect you see when the spell happens.  Can be "*" for none.
            "%sYou regenerate.%s",
            -- spellTextself:  What you see, when you cast the spell.  (split for casting on self and others)
            "*",
            -- spellTextRoom:  What the room not including you and the victim see
            "*",
            -- spellTextVictim:   What the victim sees. (not shown to self)
            "*",
            -- spellWearOff:  The text seen when a duration spell wears off.  ("*" if not a duration spell)
            "%sThe regeneration stops.%s",
            -- statusText:    Spell Status Text (when typing stats
            "%sYou are regenrating.%s"
);