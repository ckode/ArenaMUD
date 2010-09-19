del *.db
sqlite3 rooms.db ".read roomsetup.sql"
sqlite3 rooms.db ".read roomdata.sql"
sqlite3 players.db ".read playersetup.sql"
sqlite3 rcdata.db ".read rcsetup.sql"