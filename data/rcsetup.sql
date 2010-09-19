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