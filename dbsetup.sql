CREATE TABLE players (
    id                INTEGER PRIMARY KEY,
    name              VARCHAR(15) NOT NULL UNIQUE,
    lastname          VARCHAR(20) NOT NULL,
    passwd            VARCHAR(20) NOT NULL,
    hp                INTEGER NOT NULL,
    mana              INTEGER NOT NULL,
    mr                INTEGER NOT NULL,
    stealth           INTEGER NOT NULL,
    room              INTEGER NOT NULL
);

CREATE TABLE rooms (
    id                INTEGER PRIMARY KEY,
    name              VARCHAR(30) NOT NULL,
    description       VARCHAR(255) NOT NULL,
    exit_n            INTEGER NOT NULL,
    exit_ne           INTEGER NOT NULL,
    exit_e            INTEGER NOT NULL,
    exit_se           INTEGER NOT NULL,
    exit_s            INTEGER NOT NULL,
    exit_sw           INTEGER NOT NULL,
    exit_w            INTEGER NOT NULL,
    exit_nw           INTEGER NOT NULL,
    exit_u            INTEGER NOT NULL,
    exit_d            INTEGER NOT NULL,
    exits             VARCHAR(25) NOT NULL
);