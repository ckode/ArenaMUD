-- MessageTypes:
-- 1 No assigned yet
-- 2 Door open/close messages

-- Door Types

INSERT INTO messages (id, message, BriefDesc, MessageType) values (41,  "door|closed door|open door", "message for door and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (42,  "gate|closed gate|open gate", "message for gate and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (43,  "trap door|open trap door", "message for trap door and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (44,  "wall|wall|open secret passage", "message for secret passage and obvious exits", 2);
INSERT INTO messages (id, message, BriefDesc, MessageType) values (45,  "wall|BLANK|BLANK", "Just an passage, no messages", 2);