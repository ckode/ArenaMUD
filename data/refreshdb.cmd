del *.db
del *.map
sqlite3 rooms.db ".read roomsetup.sql"
sqlite3 rooms.db ".read roomdata.sql"
sqlite3 players.db ".read playersetup.sql"
sqlite3 rcdata.db ".read rcsetup.sql"
sqlite3 rcdata.db ".read rcdata.sql"
sqlite3 messages.db ".read textblocks.sql"
sqlite3 messages.db ".read messages.sql"
sqlite3 rcdata.db ".read spellsetup.sql"
sqlite3 rcdata.db ".read playerspells.sql"
sqlite3 test.map ".read roomsetup.sql"
sqlite3 test.map ".read roomdata.sql"
sqlite3 crypt.map ".read crypt.sql"
sqlite3 tower.map ".read roomsetup.sql"
sqlite3 tower.map ".read tower.sql"
