


# List of all races
RaceTable = {}
###################################
# Minions Race class
###################################
class Race():
   def __init__(self):
       self.race_id          = 0
       self.name             = ""
       self.desc             = 0      # TextBlock ID
       self.hpBonus          = 0
       self.xpTable          = 0

       self.baseStr          = 0
       self.maxStr           = 0
       self.baseAgil         = 0
       self.maxAgil          = 0
       self.baseInt          = 0
       self.maxInt           = 0
       self.baseWis          = 0
       self.maxWis           = 0
       self.baseHealth       = 0
       self.maxHealth        = 0
       self.baseCharm        = 0
       self.maxCharm         = 0

       # List of all *other* attributes from the Attributes list
       self.Attributes       = {}


# List of all races
ClassTable = {}
###################################
# Minions Race class
###################################
class Class():
   def __init__(self):
       self.class_id         = 0
       self.name             = ""
       self.desc             = 0      # TextBlock ID
       self.hpBonus          = 0
       self.xpTable          = 0

       self.minLevelHP       = 0
       self.maxLevelHP       = 0
       self.ArmorType        = 0
       self.WeaponType       = 0
       self.baseInt          = 0
       self.MageryType       = 0
       self.MageryLevel      = 0

       # List of all *other* attributes from the Attributes list
       self.Attributes       = {}
