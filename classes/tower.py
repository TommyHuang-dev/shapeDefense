import math
from functions import towerParse

# defines the tower class, which consists of two sprites: base (not rotating) and turret (rotating)
# tower types are taken from the data/towerData file

class Turret:
    def __init__(self, name):
        self.stats = towerParse.get_stats(name)  # dictionary of stats and their value

        # keeping track of tower and stat levels
        # initialize stats
        self.name = name
        self.towerLevel = 1
        self.dmgLevel = 1
        self.rateLevel = 1
        self.rangeLevel = 1  # also includes projectile speed
        self.core = 'none'

        # module effect stats
        self.dmgBoost = 0
        self.rateBoost = 0
        self.rangeBoost = 0
        self.projBoost = 0

        # initialize stats from towerParse
        self.cost = self.stats['cost']
        self.initialUpCost = self.stats['up_cost']
        self.upCostInc = self.stats['up_cost_inc']
        self.finalUpCost = self.stats['up_cost']

        # initialize tower stats
        self.maxLevel = self.stats['max_level']
        self.damage = 0  # array of tower damage by level
        self.rate = 0
        self.range = 0
        self.projSpd = 0

        # pictures and sounds
        self.spriteBase = self.stats['sprite_base']
        self.spriteTurret = self.stats['sprite_base']
        self.spriteProjectile = self.stats['sprite_base']
        self.hitSound = self.stats['hit_sound']

        # update all stats to match da level one
        self.update_stats(self.initialUpCost, self.upCostInc, self.towerLevel,
                          self.dmgLevel, self.rateLevel, self.rangeLevel)
        self.placed = False  # becomes true after the tower is placed down

    def update_stats(self, init_up, inc_up, cur_level, dmgl, ratel, rangel):
        self.finalUpCost = init_up + inc_up * (cur_level - 1)
        self.damage = self.stats['damage'][dmgl] * (1 + self.dmgBoost)
        self.rate = self.stats['rate'][ratel] * (1 + self.rateBoost)
        self.range = self.stats['range'][rangel] * (1 + self.rangeBoost)
        self.projSpd = self.stats['proj_spd'][rangel] * (1 + self.projBoost)

    def calc_boost(self, adjTowerList):
        self.dmgBoost = 0
        self.rateBoost = 0
        self.rangeBoost = 0
        self.projBoost = 0

        for i in range(len(adjTowerList)):
            if type(adjTowerList[i]) == Booster:
                if Booster.type == "damage":
                    self.dmgBoost += Booster.val
                if Booster.type == "rate":
                    self.rateBoost += Booster.val
                if Booster.type == "range":
                    self.rangeBoost += Booster.val
                if Booster.type == "projectile":
                    self.projBoost += Booster.val


    def upgrade(self, stat_name):
        self.towerLevel += 1
        if stat_name == "damage":
            self.dmgLevel += 1
        elif stat_name == "rate":
            self.rateLevel += 1
        elif stat_name == "range":
            self.rangeLevel += 1

        self.update_stats(self.initialUpCost, self.upCostInc, self.towerLevel,
                          self.dmgLevel, self.rateLevel, self.rangeLevel)

    def fire_projectile(self):
        pass


    def upgrade_on_core(self):
        pass

class Booster:
    type = "asdf"
    val = 0

