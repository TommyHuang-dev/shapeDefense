import math
import pygame
from pygame import gfxdraw
from functions import towerParse


def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


# defines the tower class, which consists of two sprites: base (not rotating) and turret (rotating)
# tower types are taken from the data/towerData file
class Turret(object):
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
        self.energy = int(self.stats['energy'][0])
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
        self.spriteBase = load_pics("images/towers/", str(self.stats['sprite_base'][0]))
        self.spriteGun = load_pics("images/towers/", str(self.stats['sprite_turret'][0]))
        self.spriteProj = load_pics("images/towers/", str(self.stats['sprite_proj'][0]))
        self.hitSound = pygame.mixer.Sound("sounds/game/" + str(self.stats['hit_sound'][0]) + ".wav")

        # update all stats to match da level one
        self.update_stats(self.initialUpCost, self.upCostInc, self.towerLevel,
                          self.dmgLevel[0], self.rateLevel[0], self.rangeLevel[0])
        self.placed = False  # becomes true after the tower is placed down
        self.pos = [0, 0]

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

    # draws a full turret, centered on a xy coordinate. The first picture is assumed to be the base.
    # rotation is an angle in radians that the turret should rotate
    def draw_tower(self, display, xy, rotation):
        # draw base
        temp = self.spriteBase.get_rect()
        display.blit(self.spriteBase, (xy[0] - temp[2] // 2, xy[1] - temp[3] // 2))
        # draw gun
        temp = self.spriteGun.get_rect()
        display.blit(self.spriteGun, (xy[0] - temp[2] // 2, xy[1] - temp[3] // 2))

    # draws a range around the tower
    def draw_range(self, display, valid, xy=0):
        # colours
        col_range_valid = [175, 200, 175, 50]
        col_range_valid_outline = [50, 50, 50, 225]
        col_range_invalid = [200, 25, 25, 30]
        col_range_invalid_outline = [125, 0, 0, 150]

        # if xy was not chosen, use the towers xy
        if xy == 0:
            xy = [self.pos[0] * 50 - 25, self.pos[1] * 50 - 25]

        # draw the range :D
        if valid:
            pygame.gfxdraw.aacircle(display, xy[0], xy[1], int(self.range * 50),
                                    col_range_valid_outline)
            pygame.gfxdraw.filled_circle(display, xy[0], xy[1], int(self.range * 50), col_range_valid)
        elif not valid:
            pygame.gfxdraw.aacircle(display, xy[0], xy[1], int(self.range * 50),
                                    col_range_invalid_outline)
            pygame.gfxdraw.filled_circle(display, xy[0], xy[1], int(self.range * 50),
                                         col_range_invalid)

class Booster:
    cost = 0
    type = "asdf"
    val = 0

    def __init__(self, asdf):
        pass
