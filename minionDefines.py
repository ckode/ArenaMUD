import string
# Game player status defines
LOGOUT           = 0
LOGIN            = 1
GETNAME          = 2
PLAYING          = 3
GETPASSWORD      = 4
COMPAREPASSWORD  = 5
NEW              = 6
EDIT             = 50

# All allowable printable characters (and BACKSPACE!)
PRINTABLE_CHARS = string.printable + chr(0x08)

#############ANSI defines################
#          Foreground Colors
RESET              = chr(27) + "[0m"
BOLD               = chr(27) + "[1m"
ITALIC             = chr(27) + "[3m"
UNDERLINE          = chr(27) + "[4m"
INVERSE            = chr(27) + "[7m"
STRIKE             = chr(27) + "[9m"
BOLD_OFF           = chr(27) + "[22m"
ITALIC_OFF         = chr(27) + "[23m"
UNDERLINE_OFF      = chr(27) + "[24m"
INVERSE_OFF        = chr(27) + "[27m"
STRIKE_OFF         = chr(27) + "[29m"
BLACK              = chr(27) + "[30m"
RED                = chr(27) + "[31m"
GREEN              = chr(27) + "[32m"
YELLOW             = chr(27) + "[33m"
BLUE               = chr(27) + "[34m"
MAGENTA            = chr(27) + "[35m"
CYAN               = chr(27) + "[36m"
WHITE              = chr(27) + "[37m"
DEFAULT            = chr(27) + "[39m"
#        Light Foreground Colors
LRED               = chr(27) + "[1;31m"
LGREEN             = chr(27) + "[1;32m"
LYELLOW            = chr(27) + "[1;33m"
LBLUE              = chr(27) + "[1;34m"
LMAGENTA           = chr(27) + "[1;35m"
LCYAN              = chr(27) + "[1;36m"
#          Background Colors
B_BLACK            = chr(27) + "[40m"
B_RED              = chr(27) + "[41m"
B_GREEN            = chr(27) + "[42m"
B_YELLOW           = chr(27) + "[43m"
B_BLUE             = chr(27) + "[44m"
B_MAGENTA          = chr(27) + "[45m"
B_CYAN             = chr(27) + "[46m"
B_WHITE            = chr(27) + "[47m"
B_DEFAULT          = chr(27) + "[49m"

########### Command Numbers #############
COMMANDS =       { '/quit':        0,
                   'who':          1,
                   'gossip':       2,
                   'say':          3,
                   'emote':        4,
                   'help':         5,
                   'set password': 6,
                   'set lastname': 7,
                   'look':         8
                 }

########### Command List ################
COMMAND_DEFS  = { 0:            "Disconnect from the game.",
                  1:            "Who is in the game.",
                  2:            "Used to gossip to everyone in the game.",
                  3:            "Use to say something or just type your mesage.",
                  4:            "Used to make your own action.",
                  5:            "Command used to list commands.",
                  6:            "Change password: 'set password <password>'",
                  7:            "Change lastname: 'set lastname <lastname>'",
                  8:            "Allows you to look around the room."
                }

