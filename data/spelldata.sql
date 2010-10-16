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


INSERT INTO spells_items (id, name, cmd, casted, use, reqClass, duration, effects, guesture, effectText, spellTextSelf, spellTextRoom, spellTextVictim, spellWearOff) VALUES
                 ( 1,                                          -- spell/item ID
                   "healing",                                  -- name
                   "heal",                                     -- Command to evoke (get for items in room)
                   1,                                          -- Is it picked up or casted (picked up 0, casted 1)
                   2,                                          -- 1 self, 2 both, 3 other person
                   "4",                                        -- List of class IDs separated by ":"
                   0,                                          -- How long it lasts 0 = instant like a single heal (if duration > 0 effects can go above max stat)
                   "1:10",                                     -- Stored as "stat: value" say HP = 1 "1: 20" would add 20HP
                   "*",                                        -- if item, %s picks up, if spell, makes guesture. separate self / room with "|" (or use "*" to ignore)
                   "*",                                        -- Text seen when duration effect happens. self only. (you feel better single heal, or You feel sick fo poison etc
                   "%sYou cast healing on %s!%s",              -- Text displayed to self
                   "%s%s cast healing on %s!%s",               -- Text displayed to room
                   "%s%s cast healing on you!%s",              -- Text displayed to person casted upon, set as "*" if self cast only or picked up item
                   "*"                                         -- Wear off text if duration spell "*" if not.
);


INSERT INTO spells_items (id, name, cmd, casted, use, reqClass, duration, effects, guesture, effectText, spellTextSelf, spellTextRoom, spellTextVictim, spellWearOff) VALUES
                 ( 2,                                          -- spell/item ID
                   "glob of frost",                            -- name
                   "fros",                                     -- Command to evoke (get for items in room)
                   1,                                          -- Is it picked up or casted (picked up 0, casted 1)
                   3,                                          -- 1 self, 2 both, 3 other person
                   "2",                                        -- List of class IDs separated by ":"
                   10,                                         -- How long it lasts 0 = instant like a single heal (if duration > 0 effects can go above max stat)
                   "1:-2",                                     -- Stored as "stat: value" say HP = 1 "1: 20" would add 20HP
                   "*",                                        -- if item, %s picks up, if spell, makes guesture. separate self / room with "|" (or use "*" to ignore)
                   "%sYou are freezing.%s",                    -- Text seen when duration effect happens. self only. (you feel better single heal, or You feel sick fo poison etc
                   "%sYou cast glob of frost on %s!%s",        -- Text displayed to self
                   "%s%s cast glob of frost on %s!%s",         -- Text displayed to room
                   "%s%s cast glob of frost on you!%s",        -- Text displayed to person casted upon, set as "*" if self cast only or picked up item
                   "%sYou are no longer freezing%s"            -- Spell wears off text if duration spell, if not use "*".
);