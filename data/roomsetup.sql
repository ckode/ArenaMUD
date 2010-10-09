CREATE TABLE rooms (
    id                INTEGER PRIMARY KEY,       -- Door ID
    name              VARCHAR(30) NOT NULL,
    desc1             VARCHAR(75) NOT NULL,      -- Room Long Description line 1
    desc2             VARCHAR(75) NOT NULL,      -- Room Long Description line 2
    desc3             VARCHAR(75) NOT NULL,      -- Room Long Description line 3
    desc4             VARCHAR(75) NOT NULL,      -- Room Long Description line 4
    desc5             VARCHAR(75) NOT NULL,      -- Room Long Description line 5
    doors             VARCHAR(75) NOT NULL,      -- List of door numbers split with |
    light             INTEGER NOT NULL,          -- Light Level (1 normal, 2 nightvision, 3 dark vision)
    roomspell         INTEGER NOT NULL,          -- spell that always casts in room
    trap              INTEGER NOT NULL,          -- trap that hits when someone enters the room
    nospawn           INTEGER NOT NULL           -- Zero you can spawn in this room, 1 you cannot
);

CREATE TABLE Doors (
    id                INTEGER PRIMARY KEY,       -- Door ID
    DoorType          INTEGER NOT NULL,          -- PATHWAY, Gate, S
    Passable          INTEGER NOT NULL,
    DoorStatus        INTEGER NOT NULL,          -- 1 open, 2 closed
    DoesLock          INTEGER NOT NULL,
    Locked            INTEGER NOT NULL,
    DoorDesc          INTEGER NOT NULL,
    ExitRoom1         INTEGER NOT NULL,
    ExitRoom2         INTEGER NOT NULL
);

CREATE TABLE RoomSpells (
    id                INTEGER PRIMARY KEY,
    hp_adjust         INTEGER NOT NULL,
    desc              VARCHAR(75) NOT NULL,
    name              VARCHAR(25) NOT NULL
);

CREATE TABLE RoomTraps (
    id                INTEGER PRIMARY KEY,
    stat              INTEGER NOT NULL,
    value             INTEGER NOT NULL,
    duration          INTEGER NOT NULL,
    playerdesc        VARCHAR(75) NOT NULL,
    roomdesc          VARCHAR(75) NOT NULL,
    name              VARCHAR(25) NOT NULL
);
