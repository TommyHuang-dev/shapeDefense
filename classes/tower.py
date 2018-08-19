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
        self.type = self.stats['type'][0]
        self.targeting = self.stats['targeting'][0]
        self.towerLevel = 1
        self.dmgLevel = [1, len(self.stats['damage'])]
        self.rateLevel = [1, len(self.stats['rate'])]
        self.rangeLevel = [1, len(self.stats['range'])]  # also includes projectile speed

        # module effect stats
        self.dmgBoost = 0
        self.rateBoost = 0
        self.rangeBoost = 0
        self.projBoost = 0

        # initialize stats from towerParse
        self.cost = int(self.stats['cost'][0])
        self.initialUpCost = int(self.stats['up_cost'][0])
        self.upCostInc = int(self.stats['up_cost_inc'][0])
        self.finalUpCost = int(self.stats['up_cost'][0])
        self.special = self.stats['special'][0]
        self.specialVal = self.stats['special_val'][0]
        # range * effRange = how far the projectile actually goes
        self.effRange = float(self.stats['effective_range'][0])

        # initialize tower stats
        self.maxLevel = int(self.stats['max_level'][0])
        self.damage = 0  # array of tower damage by level
        self.rate = 0
        self.range = 0  # range that it will target enemies
        self.projSpd = 0

        # pictures and sounds
        self.spriteBase = str(self.stats['sprite_base'][0])
        self.spriteTurret = str(self.stats['sprite_base'][0])
        self.spriteProjectile = str(self.stats['sprite_base'][0])
        self.hitSound = str(self.stats['hit_sound'][0])

        # update all stats to match da level one
        self.update_stats(self.initialUpCost, self.upCostInc, self.towerLevel,
                          self.dmgLevel[0], self.rateLevel[0], self.rangeLevel[0])
        self.placed = False  # becomes true after the tower is placed down

    def update_stats(self, init_up, inc_up, cur_level, dmgl, ratel, rangel):
        self.finalUpCost = int(init_up + inc_up * (cur_level - 1))
        self.damage = int(self.stats['damage'][dmgl - 1] * (1 + self.dmgBoost))
        self.rate = float(self.stats['rate'][ratel - 1] * (1 + self.rateBoost))
        self.range = float(self.stats['range'][rangel - 1] * (1 + self.rangeBoost))
        self.projSpd = float(self.stats['proj_spd'][rangel - 1] * (1 + self.projBoost))

    def calc_boost(self, adj_tower_list):
        self.dmgBoost = 0
        self.rateBoost = 0
        self.rangeBoost = 0
        self.projBoost = 0

        for i in range(len(adj_tower_list)):
            if type(adj_tower_list[i]) == Booster:
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
                          self.dmgLevel[0], self.rateLevel[0], self.rangeLevel[0])

    def fire_projectile(self):
        pass

    def upgrade_on_core(self):
        pass


class Booster:
    type = "asdf"
    val = 0

    def __init__(self, asdf):
        pass
