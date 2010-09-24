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
    trap              INTEGER NOT NULL           -- trap that hits when someone enters the room
);

CREATE TABLE Doors (
    id                INTEGER PRIMARY KEY,       -- Door ID
    DoorType          INTEGER NOT NULL,
    Passable          INTEGER NOT NULL,
    DoorStatus        INTEGER NOT NULL,
    DoesLock          INTEGER NOT NULL,
    Locked            INTEGER NOT NULL,
    DoorDesc          INTEGER NOT NULL,
    ExitRoom1         INTEGER NOT NULL,
    ExitRoom2         INTEGER NOT NULL
);


