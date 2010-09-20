CREATE TABLE messages (
   id                 INTEGER PRIMARY KEY,
   message            VARCHAR(256) NOT NULL,
   BriefDesc          VARCHAR(1024)              -- Brief explination of what this text block belongs too! (not used in game, only reference)
);

