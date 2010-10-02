CREATE TABLE race (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(15) NOT NULL UNIQUE,
   description        INTEGER NOT NULL,         -- TextBlock ID
   BaseHP             INTEGER NOT NULL,
   DamageBonus        INTEGER NOT NULL,         -- Damage Bonus
   CastingBonus       INTEGER NOT NULL,         -- Casting bonus (better caster?)
   Vision             INTEGER NOT NULL,         -- 1 normal, 2 night, 3 DARK vision
   DefenseBonus       INTEGER NOT NULL,         -- Makes you harder to hit
   ToHitBonus         INTEGER NOT NULL,         -- Makes you more accurate
   Stealth            INTEGER NOT NULL          -- Bonus to stealth if class has stealth
);

CREATE TABLE class (
   id                 INTEGER PRIMARY KEY,
   name               VARCHAR(15) NOT NULL UNIQUE,
   description        INTEGER NOT NULL,         -- TextBlock ID
   HPBonus            INTEGER NOT NULL,
   MinDamage          INTEGER NOT NULL,
   MaxDamage          INTEGER NOT NULL,
   BaseArmor          INTEGER NOT NULL,
   MageryType         INTEGER NOT NULL,
   Stealth            INTEGER NOT NULL,
   WeaponMessages     INTEGER NOT NULL
);