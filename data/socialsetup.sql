#  ArenaMUD - A multiplayer combat game - http://arenamud.david-c-brown.com
#  Copyright (C) 2009, 2010 - David C Brown & Mark Richardson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


CREATE TABLE socialaction (
     ActionType         = INTEGER NOT NULL,
     cmd                = VARCHAR(15) NOT NULL,
     minCmdGTLen        = INTEGER NOT NULL,
     minCmds            = INTEGER NOT NULL,
     helpDesc           = VARCHAR(1024) NOT NULL,
     selfOnlyMe         = VARCHAR(250) NOT NULL,
     selfOnlyRoom       = VARCHAR(250) NOT NULL,
     VictMe             = VARCHAR(250) NOT NULL,
     VictVict           = VARCHAR(250) NOT NULL,
     VictRoom           = VARCHAR(250) NOT NULL
);