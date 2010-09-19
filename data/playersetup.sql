CREATE TABLE players (
    id                INTEGER PRIMARY KEY,
    name              VARCHAR(15) NOT NULL UNIQUE,
    lastname          VARCHAR(20) NOT NULL,
    passwd            VARCHAR(20) NOT NULL,
    hp                INTEGER NOT NULL,
    maxhp             INTEGER NOT NULL,
    mana              INTEGER NOT NULL,
    maxmana           INTEGER NOT NULL,
    mr                INTEGER NOT NULL,
    stealth           INTEGER NOT NULL,
    room              INTEGER NOT NULL
);

CREATE TABLE PlayerAttrs (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(30) NOT NULL,
   BriefDesc          VARCHAR(1024) NOT NULL    -- Brief explination of what this text block belongs too! (not used in game, only reference)
);