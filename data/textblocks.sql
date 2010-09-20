CREATE TABLE messages (
   id                 INTEGER PRIMARY KEY,
   message            VARCHAR(256) NOT NULL,
   BriefDesc          VARCHAR(1024),              -- Brief explination of what this text block belongs too! (not used in game, only reference
   MessageType        INTEGER NOT NULL           -- Message type tells what type of message it is, not for game but finding specific messages of type
);

