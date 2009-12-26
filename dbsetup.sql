CREATE TABLE players (
    id                INTEGER PRIMARY KEY,
    name              VARCHAR(15) NOT NULL,
    lastname          VARCHAR(20) NOT NULL,
    passwd            VARCHAR(20) NOT NULL,
    hp                INTEGER NOT NULL,
    mana              INTEGER NOT NULL,
    mr                INTEGER NOT NULL,
    stealth           INTEGER NOT NULL
);