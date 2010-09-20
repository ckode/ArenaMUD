-- MessageTypes:
-- 1 Moving messages
-- 2 Door open/close messages

-- Generic moving messages

INSERT INTO messages (id, message, BriefDesc, MessageType) values (1,  " leaves to the north.| walks in from the south.|You run into the wall to the north!| runs into the wall to the north!", "For when a player walks north.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (2,  " leaves to the northeast.| walks in from the southwest.|You run into the wall to the northeast!| runs into the wall to the northeast!", "For when a player walks northeast.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (3,  " leaves to the east.| walks in from the west.|You run into the wall to the east!| runs into the wall to the east!", "For when a player walks east.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (4,  " leaves to the southeast.| walks in from the northwest.|You run into the wall to the southeast!| runs into the wall to the southeast!", "For when a player walks southeast.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (5,  " leaves to the south.| walks in from the north.|You run into the wall to the south!| runs into the wall to the south!", "For when a player walks south.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (6,  " leaves to the southwest.| walks in from the northeast.|You run into the wall to the southwest!| runs into the wall to the southwest!", "For when a player walks southwest.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (7,  " leaves to the west.| walks in from the east.|You run into the wall to the west!| runs into the wall to the west!", "For when a player walks west.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (8,  " leaves to the northwest.| walks in from the southeast.|You run into the wall to the northwest!| runs into the wall to the northwest!", "For when a player walks northwest.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (9,  " leaves up.| arrives from below.|You run into the wall above!| runs into the wall above!", "For when a player tries to go up.", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (10, " leaves down.| arrives from above.|You run into the floor!| runs into the floor!", "For when a player tries to go down.", 1);

-- Gates moving messages

INSERT INTO messages (id, message, BriefDesc, MessageType) values (11,  " leaves to the north.| walks in from the south.|You run into the gate to the north!| runs into the gate to the north!", "For when a player walks north. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (12,  " leaves to the northeast.| walks in from the southwest.|You run into the gate to the northeast!| runs into the gate to the northeast!", "For when a player walks northeast. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (13,  " leaves to the east.| walks in from the west.|You run into the gate to the east!| runs into the gate to the east!", "For when a player walks east. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (14,  " leaves to the southeast.| walks in from the northwest.|You run into the gate to the southeast!| runs into the gate to the southeast!", "For when a player walks southeast. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (15,  " leaves to the south.| walks in from the north.|You run into the gate to the south!| runs into the gate to the south!", "For when a player walks south. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (16,  " leaves to the southwest.| walks in from the northeast.|You run into the gate to the southwest!| runs into the gate to the southwest!", "For when a player walks southwest. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (17,  " leaves to the west.| walks in from the east.|You run into the gate to the west!| runs into the gate to the west!", "For when a player walks west. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (18,  " leaves to the northwest.| walks in from the southeast.|You run into the gate to the northwest!| runs into the gate to the northwest!", "For when a player walks northwest. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (19,  " leaves up.| arrives from below.|You run into the gate above!| runs into the gate above!", "For when a player tries to go up. (gate)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (20,  " leaves down.| arrives from above.|You run into the gate below!| runs into the gate below!", "For when a player tries to go down. (gate)", 1);

-- Doors moving messages

INSERT INTO messages (id, message, BriefDesc, MessageType) values (21,  " leaves to the north.| walks in from the south.|You run into the door to the north!| runs into the door to the north!", "For when a player walks north. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (22,  " leaves to the northeast.| walks in from the southwest.|You run into the door to the northeast!| runs into the door to the northeast!", "For when a player walks northeast. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (23,  " leaves to the east.| walks in from the west.|You run into the door to the east!| runs into the door to the east!", "For when a player walks east. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (24,  " leaves to the southeast.| walks in from the northwest.|You run into the door to the southeast!| runs into the door to the southeast!", "For when a player walks southeast. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (25,  " leaves to the south.| walks in from the north.|You run into the door to the south!| runs into the door to the south!", "For when a player walks south. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (26,  " leaves to the southwest.| walks in from the northeast.|You run into the door to the southwest!| runs into the door to the southwest!", "For when a player walks southwest. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (27,  " leaves to the west.| walks in from the east.|You run into the door to the west!| runs into the door to the west!", "For when a player walks west. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (28,  " leaves to the northwest.| walks in from the southeast.|You run into the door to the northwest!| runs into the door to the northwest!", "For when a player walks northwest. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (29,  " leaves up.| arrives from below.|You run into the door above!| runs into the door above!", "For when a player tries to go up. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (30,  " leaves down.| arrives from above.|You run into the door below!| runs into the door below!", "For when a player tries to go down. (door)", 1);

-- Doors moving messages

INSERT INTO messages (id, message, BriefDesc, MessageType) values (31,  " leaves to the north.| walks in from the south.|You run into the door to the north!| runs into the door to the north!", "For when a player walks north. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (32,  " leaves to the northeast.| walks in from the southwest.|You run into the door to the northeast!| runs into the door to the northeast!", "For when a player walks northeast. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (33,  " leaves to the east.| walks in from the west.|You run into the door to the east!| runs into the door to the east!", "For when a player walks east. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (34,  " leaves to the southeast.| walks in from the northwest.|You run into the door to the southeast!| runs into the door to the southeast!", "For when a player walks southeast. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (35,  " leaves to the south.| walks in from the north.|You run into the door to the south!| runs into the door to the south!", "For when a player walks south. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (36,  " leaves to the southwest.| walks in from the northeast.|You run into the door to the southwest!| runs into the door to the southwest!", "For when a player walks southwest. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (37,  " leaves to the west.| walks in from the east.|You run into the door to the west!| runs into the door to the west!", "For when a player walks west. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (38,  " leaves to the northwest.| walks in from the southeast.|You run into the door to the northwest!| runs into the door to the northwest!", "For when a player walks northwest. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (39,  " leaves up.| arrives from below.|You run into the door above!| runs into the door above!", "For when a player tries to go up. (door)", 1);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (40,  " leaves down.| arrives from above.|You run into the door below!| runs into the door below!", "For when a player tries to go down. (door)", 1);

-- Door Types

INSERT INTO messages (id, message, BriefDesc, MessageType) values (41,  "closed door|open door", "message for door and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (42,  "closed gate|open gate", "message for gate and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (43,  "trade door|open trade door", "message for trap door and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (44,  "BLANK|open secret passage", "message for secret passage and obvious exits", 2);