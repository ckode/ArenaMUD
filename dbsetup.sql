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


CREATE TABLE TextBlock (
   id                 INTEGER PRIMARY KEY,
   TextBlock          VARCHAR(4096) NOT NULL,
   BriefDesc          VARCHAR(1024) NOT NULL    -- Brief explination of what this text block belongs too! (not used in game, only reference)
);

CREATE TABLE PlayerAttrs (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(30) NOT NULL,
   BriefDesc          VARCHAR(1024) NOT NULL    -- Brief explination of what this text block belongs too! (not used in game, only reference)
);

CREATE TABLE Messages (
   id                 INTEGER PRIMARY KEY,
   player             VARCHAR(256) NOT NULL,
   victiom            VARCHAR(256) NOT NULL,
   otherplayers       VARCHAR(256) NOT NULL,
   entireroom         VARCHAR(256) NOT NULL
);

CREATE TABLE race (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(15) NOT NULL UNIQUE,
   description        INTEGER NOT NULL,         -- TextBlock ID
   HPBonus            INTEGER NOT NULL,
   XPTable            INTEGER NOT NULL,
   BaseStr            INTEGER NOT NULL,
   MaxStr             INTEGER NOT NULL,
   BaseAgil           INTEGER NOT NULL,
   MaxAgil            INTEGER NOT NULL,
   BaseInt            INTEGER NOT NULL,
   MaxInt             INTEGER NOT NULL,
   BaseWis            INTEGER NOT NULL,
   MaxWis             INTEGER NOT NULL,
   BaseHealth         INTEGER NOT NULL,
   MaxHealth          INTEGER NOT NULL,
   BaseCharm          INTEGER NOT NULL,
   MaxCharm           INTEGER NOT NULL,
   Attribures         VARCHAR(1024) NOT NULL     -- string of attributes ( AttrID,Value )combos split by PIPES. ie "1,15|2,35|24,5"
);

CREATE TABLE class (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(15) NOT NULL UNIQUE,
   description        INTEGER NOT NULL,         -- TextBlock ID
   XPTable            INTEGER NOT NULL,
   MinLevelHP         INTEGER NOT NULL,
   MaxLevelHP         INTEGER NOT NULL,
   Combat             INTEGER NOT NULL,
   ArmorType          INTEGER NOT NULL,
   WeaponsType        INTEGER NOT NULL,
   MageryType         INTEGER NOT NULL,
   MageryLevel        INTEGER NOT NULL,
   Attribures         VARCHAR(1024) NOT NULL     -- string of attributes ( AttrID,Value )combos split by PIPES. ie "1,15|2,35|24,5"
);


CREATE TABLE rooms (
    id                INTEGER PRIMARY KEY,       -- Room ID
    name              VARCHAR(30) NOT NULL,      -- Room Short Description
    desc1             VARCHAR(75) NOT NULL,      -- Room Long Description line 1
    desc2             VARCHAR(75) NOT NULL,      -- Room Long Description line 2
    desc3             VARCHAR(75) NOT NULL,      -- Room Long Description line 3
    desc4             VARCHAR(75) NOT NULL,      -- Room Long Description line 4
    desc5             VARCHAR(75) NOT NULL,      -- Room Long Description line 5
    RoomType          INTEGER NOT NULL,          -- Room Type (normal, regen, shop, Hall of the Dead, etc
    light             INTEGER NOT NULL,          -- Light Level (1 normal, 2 nightvision, 3 dark vision)
    phrase            VARCHAR(20) NOT NULL,      -- Secret phrase that changes something in room.
    PhraseFunction    INTEGER NOT NULL,          -- Links to a command list
    actionID          INTEGER NOT NULL,          -- Phrase action text
  ---- North Door
    N_TYPE            INTEGER NOT NULL,          -- Room Type (0 No door, 1 path way, 2 actual Door, 3 secret door)
    N_ROOM            INTEGER NOT NULL,          -- Room Number that the door leads too
    N_STATUS          INTEGER NOT NULL,          -- Room Status (for views) 0 door not shown (hidden), 1 show exit text1, 2 show exit text2
    N_LOCK            INTEGER NOT NULL,          -- Is the door lockable? (require lock picking or key)
    N_KEY             INTEGER NOT NULL,          -- Key ID required to unlock
    N_PICKDIFF        INTEGER NOT NULL,          -- Difficulty to pick
    N_PASSABLE        INTEGER NOT NULL,          -- Passable by default (0 No, 1 yes) Actual doors and secret doors should default to No.
    N_EXIT1           VARCHAR(15) NOT NULL,      -- Default visable text.  (north, west, trap door down, etc)
    N_EXIT2           VARCHAR(15) NOT NULL,      -- Alternate text (if door is open, door open west, open trap door down, etc)
  ---- Northeast Door
    NE_TYPE           INTEGER NOT NULL,
    NE_ROOM           INTEGER NOT NULL,
    NE_STATUS         INTEGER NOT NULL,
    NE_LOCK           INTEGER NOT NULL,
    NE_KEY            INTEGER NOT NULL,
    NE_PICKDIFF       INTEGER NOT NULL,
    NE_PASSABLE       INTEGER NOT NULL,
    NE_EXIT1          VARCHAR(15) NOT NULL,
    NE_EXIT2          VARCHAR(15) NOT NULL,
  ---- East Door
    E_TYPE            INTEGER NOT NULL,
    E_ROOM            INTEGER NOT NULL,
    E_STATUS          INTEGER NOT NULL,
    E_LOCK            INTEGER NOT NULL,
    E_KEY             INTEGER NOT NULL,
    E_PICKDIFF        INTEGER NOT NULL,
    E_PASSABLE        INTEGER NOT NULL,
    E_EXIT1           VARCHAR(15) NOT NULL,
    E_EXIT2           VARCHAR(15) NOT NULL,
  ---- Southeast Door
    SE_TYPE           INTEGER NOT NULL,
    SE_ROOM           INTEGER NOT NULL,
    SE_STATUS         INTEGER NOT NULL,
    SE_LOCK           INTEGER NOT NULL,
    SE_KEY            INTEGER NOT NULL,
    SE_PICKDIFF       INTEGER NOT NULL,
    SE_PASSABLE       INTEGER NOT NULL,
    SE_EXIT1          VARCHAR(15) NOT NULL,
    SE_EXIT2          VARCHAR(15) NOT NULL,
  ---- South Door
    S_TYPE            INTEGER NOT NULL,
    S_ROOM            INTEGER NOT NULL,
    S_STATUS          INTEGER NOT NULL,
    S_LOCK            INTEGER NOT NULL,
    S_KEY             INTEGER NOT NULL,
    S_PICKDIFF        INTEGER NOT NULL,
    S_PASSABLE        INTEGER NOT NULL,
    S_EXIT1           VARCHAR(15) NOT NULL,
    S_EXIT2           VARCHAR(15) NOT NULL,
  ---- Southwest Door
    SW_TYPE           INTEGER NOT NULL,
    SW_ROOM           INTEGER NOT NULL,
    SW_STATUS         INTEGER NOT NULL,
    SW_LOCK           INTEGER NOT NULL,
    SW_KEY            INTEGER NOT NULL,
    SW_PICKDIFF       INTEGER NOT NULL,
    SW_PASSABLE       INTEGER NOT NULL,
    SW_EXIT1          VARCHAR(15) NOT NULL,
    SW_EXIT2          VARCHAR(15) NOT NULL,
  ---- West Door
    W_TYPE            INTEGER NOT NULL,
    W_ROOM            INTEGER NOT NULL,
    W_STATUS          INTEGER NOT NULL,
    W_LOCK            INTEGER NOT NULL,
    W_KEY             INTEGER NOT NULL,
    W_PICKDIFF        INTEGER NOT NULL,
    W_PASSABLE        INTEGER NOT NULL,
    W_EXIT1           VARCHAR(15) NOT NULL,
    W_EXIT2           VARCHAR(15) NOT NULL,
  ---- Northwest Door
    NW_TYPE           INTEGER NOT NULL,
    NW_ROOM           INTEGER NOT NULL,
    NW_STATUS         INTEGER NOT NULL,
    NW_LOCK           INTEGER NOT NULL,
    NW_KEY            INTEGER NOT NULL,
    NW_PICKDIFF       INTEGER NOT NULL,
    NW_PASSABLE       INTEGER NOT NULL,
    NW_EXIT1          VARCHAR(15) NOT NULL,
    NW_EXIT2          VARCHAR(15) NOT NULL,
  ---- Up Door
    U_TYPE            INTEGER NOT NULL,
    U_ROOM            INTEGER NOT NULL,
    U_STATUS          INTEGER NOT NULL,
    U_LOCK            INTEGER NOT NULL,
    U_KEY             INTEGER NOT NULL,
    U_PICKDIFF        INTEGER NOT NULL,
    U_PASSABLE        INTEGER NOT NULL,
    U_EXIT1           VARCHAR(15) NOT NULL,
    U_EXIT2           VARCHAR(15) NOT NULL,
  ---- Down Door
    D_TYPE            INTEGER NOT NULL,
    D_ROOM            INTEGER NOT NULL,
    D_STATUS          INTEGER NOT NULL,
    D_LOCK            INTEGER NOT NULL,
    D_KEY             INTEGER NOT NULL,
    D_PICKDIFF        INTEGER NOT NULL,
    D_PASSABLE        INTEGER NOT NULL,
    D_EXIT1           VARCHAR(15) NOT NULL,
    D_EXIT2           VARCHAR(15) NOT NULL
);

