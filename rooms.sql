INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits, altexits, phrase, secretdir, secretroom, actionID)
        values ( 1,
                 "Town Square",
                 "This is the Town Square of Dagnoroth!  You see trash piled up everywhere as the city has fallen from grace of the last few years.!",
                 1,  -- Light level (1 light, 2 dark (night vision), 3 pitch black (dark vision))
                 3,  -- N
                 0,  -- NE
                 0,  -- E
                 0,  -- SE
                 0,  -- S
                 0,  -- SW
                 0,  -- W
                 0,  -- NW
                 0,  -- U
                 2,  -- D
                 "north, down.",   -- Exits
                 "None",           -- Alternet Exits
                 "None",           -- Secret Phrase
                 0,                -- Secret exit direction
                 0,                -- Secret room number
                 0);               -- Action message when secret exit is triggered

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits, altexits, phrase, secretdir, secretroom, actionID)
        values ( 2,
                 "Hole in the Ground",
                 "This is a big hole in the ground where most of the towns people defecate.  It smells like shit!",
                 1,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 1,
                 0,
                 "up.",
                 "None",
                 "None",
                 0,
                 0,
                 0);

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits, altexits, phrase, secretdir, secretroom, actionID)
        values ( 3,
                 "Northern Sonzo Ave.",
                 "This is a northern section of the main drag of through the city of Dagnoroth!",
                 1,
                 4,
                 0,
                 0,
                 0,
                 1,
                 0,
                 0,
                 0,
                 0,
                 0,
                 "north, south.",
                 "None",
                 "None",
                 0,
                 0,
                 0);

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits, altexits, phrase, secretdir, secretroom, actionID)
        values ( 4,
                 "Northern Sonzo Ave.",
                 "This is a northern section of the main drag of through the city of Dagnoroth!",
                 1,
                 5,
                 0,
                 0,
                 0,
                 3,
                 0,
                 0,
                 0,
                 0,
                 0,
                 "north, south.",
                 "None",
                 "None",
                 0,
                 0,
                 0);

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits, altexits, phrase, secretdir, secretroom, actionID)
        values ( 5,
                 "Cornor of Northern Sonzo and Markus St.",
                 "This is a northern section of the city of Dagnoroth!",
                 1,
                 0,
                 0,
                 6,
                 0,
                 4,
                 0,
                 0,
                 0,
                 0,
                 0,
                 "south, east.",
                 "None",
                 "None",
                 0,
                 0,
                 0);

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits, altexits, phrase, secretdir, secretroom, actionID)
        values ( 6,
                 "Markus St, Dark Alley.",
                 "You are dark alley on Markus St.  This appears to be a very dangerous section of town!",
                 2,
                 0,
                 0,
                 7,
                 0,
                 0,
                 0,
                 5,
                 0,
                 0,
                 0,
                 "east, west.",
                 "None",
                 "None",
                 0,
                 0,
                 0);

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits, altexits, phrase, secretdir, secretroom, actionID)
        values ( 7,
                 "Markus St Dead End.",
                 "You are at a dead end on Markus St.  On the southern wall there appears to be a perfectly straight horizontal crack in the wall and a soft glow coming from it.  This appears to be a very dangerous section of town!",
                 3,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 6,
                 0,
                 0,
                 0,
                 "west.",
                 "west, secret passage south.",
                 "push wall",
                 5,
                 8,
                 1);

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits, altexits, phrase, secretdir, secretroom, actionID)
        values ( 8,
                 "Gang Hideout",
                 "You are in the notorious gang The PorkLord's hideout. If found here, you surly will be killed!",
                 1,
                 7,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 "north.",
                 "None",
                 "None",
                 0,
                 0,
                 0);