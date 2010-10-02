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
INSERT INTO messages (id, message, BriefDesc, MessageType) values (1, "You swing your axe at %s, but miss!|You chop %s for %i damage!|%s swings at you with an axe, but misses!|%s chops you for %i damage!|%s swings at %s, but misses!|%s chops %s for %i damage!", "Weapon messages for Barbarian", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (2, "You try to fire a magic missle at %s, but failed!|You fire a magic missle at %s for %i damage!|%s tries to fire a magic missle at you, but fails!|%s fires a magic missle at you for %i damage!|%s tries to fire a magic missle at %s, but failed!|%s fires a magic missle at %s for %i damage!", "Weapon messages for mage", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (3, "You swing your shortsword at %s, but miss!|You slice %s for %i damage!|%s swings at you with a shortsword, but misses!|%s slices you for %i damage!|%s swings at %s, but misses!|%s slices %s for %i damage!", "Weapon messages for thief", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (4, "You tries to cast holy force at %s, but failed!|You blasts %s with holy force for %i damage!|%s tries to cast holy force at you, but failed!|%s blasts you with holy force for %i damage!|%s tries to cast holy force at %s, but failed!|%s blasts %s with holy force for %i damage!", "Weapon messages for priest", 1);