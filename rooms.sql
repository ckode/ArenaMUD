INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits)
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
             --    0,  -- ?? Errors without it
                 0,  -- U
                 2,  -- D
                 "north, down.");

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits)
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
                -- 0,
                 1,
                 0,
                 "up.");

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits)
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
                -- 0,
                 0,
                 0,
                 "north, south.");

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits)
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
                -- 0,
                 0,
                 0,
                 "north, south.");

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits)
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
               --  0,
                 0,
                 0,
                 "south, east.");

INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits)
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
              --   0,
                 0,
                 0,
                 "east, west.");
                 
INSERT INTO rooms (id, name, description, light, exit_n, exit_ne, exit_e, exit_se, exit_s, exit_sw, exit_w, exit_nw, exit_u, exit_d, exits)
        values ( 7,
                 "Markus St Dead End.",
                 "You are at a dead end on Markus St.  This appears to be a very dangerous section of town!",
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
                 "west.");