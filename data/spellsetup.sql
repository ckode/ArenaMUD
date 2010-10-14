CREATE TABLE spells_items (
      id                INTEGER PRIMARY KEY,       -- Spell/Item ID
      name              VARCHAR(25) NOT NULL,      -- Item or spell name
      cmd               VARCHAR(4) NOT NULL,       -- Command used to evoke
      casted            INTEGER NOT NULL,          -- Is it picked up or casted (picked up 0, casted 1)
      use               INTEGER NOT NULL,          -- 1 self, 2 both, 3 other person
      reqClass          VARCHAR(50) NOT NULL,      -- List of class IDs separated by ":"
      duration          INTEGER NOT NULL,          -- How long it lasts 0 = instant like a single heal (if duration > 0 effects can go above max stat)
      effects           VARCHAR(50) NOT NULL,      -- Stored as "stat: value" say HP = 1 "1: 20" would add 20HP
      guesture          VARCHAR(100) NOT NULL,     -- if item, %s picks up, if spell, makes guesture. separate self / room with "|" (or use "*" to ignore)
      effectText        VARCAHR(100) NOT NULL,     -- Text seen when duration effect happens. self only. (you feel better single heal, or You feel sick fo poison etc
      spellTextself     VARCHAR(100) NOT NULL,     -- Text displayed to self
      spellTextRoom     VARCHAR(100) NOT NULL,     -- Text displayed to room
      spellTextVictim   VARCHAR(100) NOT NULL,     -- Text displayed to person casted upon, set as "*" if self cast only or picked up item
      spellWearOff      VARCHAR(100) NOT NULL      -- Wear off text if duration spell "*" if not
);

