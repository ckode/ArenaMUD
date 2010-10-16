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


INSERT INTO race (id, name, description, BaseHP, DamageBonus, CastingBonus, Vision, DefenseBonus, ToHitBonus, Stealth) VALUES (1, "Human", "A human", 100, 0, 0, 1, 0, 0, 0);
INSERT INTO race (id, name, description, BaseHP, DamageBonus, CastingBonus, Vision, DefenseBonus, ToHitBonus, Stealth) VALUES (2, "Dark-Elf", "A Dark-Elf", 90, 0, 20, 2, 5, 5, 30);
INSERT INTO race (id, name, description, BaseHP, DamageBonus, CastingBonus, Vision, DefenseBonus, ToHitBonus, Stealth) VALUES (3, "Ogre", "A Ogre", 120, 5, -25, 2, -5, -5, -30);
INSERT INTO race (id, name, description, BaseHP, DamageBonus, CastingBonus, Vision, DefenseBonus, ToHitBonus, Stealth) VALUES (4, "Goblin", "A Goblin", 80, 0, 10, 2, 10, 10, 30);


INSERT INTO class (id, name, description, HPBonus, MinDamage, MaxDamage, BaseArmor, MageryType, Stealth, WeaponMessages) VALUES (1, "Barbarian", "A barbarian", 15, 5, 20, 50, 1, 0, 1);
INSERT INTO class (id, name, description, HPBonus, MinDamage, MaxDamage, BaseArmor, MageryType, Stealth, WeaponMessages) VALUES (2, "Mage", "A Mage", 0, 5, 25, 50, 2, 0, 2);
INSERT INTO class (id, name, description, HPBonus, MinDamage, MaxDamage, BaseArmor, MageryType, Stealth, WeaponMessages) VALUES (3, "Theif", "A Thief", -15, 5, 15, 50, 0, 50, 3);
INSERT INTO class (id, name, description, HPBonus, MinDamage, MaxDamage, BaseArmor, MageryType, Stealth, WeaponMessages) VALUES (4, "Priest", "A Priest", 0, 5, 25, 50, 3, 0, 4);