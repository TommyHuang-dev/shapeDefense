import math
import pygame
from pygame import gfxdraw
from functions import towerParse
from functions import components
from classes import projectile


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
        self.rotation = math.pi / 2
        self.type = self.stats['type'][0]
        self.curLevel = 1
        self.maxLevel = int(self.stats['max_level'][0])
        self.dmgLevel = [1, len(self.stats['damage'])]
        self.rateLevel = [1, len(self.stats['rate'])]
        self.rangeLevel = [1, len(self.stats['range'])]  # also includes projectile speed
        self.specialLevel = [1, len(self.stats['special_val'])]

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
        self.sellPrice = self.cost / 2  # float, convert to int when actually selling
        self.special = self.stats['special'][0]
        self.specialVal = self.stats['special_val'][0]
        if 'special_val2' in self.stats:
            self.specialVal2 = self.stats['special_val2'][0]
        # range * effRange = how far the projectile actually goes
        self.effRange = float(self.stats['effective_range'][0])
        self.reload = 0.01

        # initialize tower stats
        self.damage = 0  # array of tower damage by level
        self.rate = 0
        self.range = 0  # range that it will target enemies
        self.projSpd = 0

        # pictures and sounds
        self.spriteBase = load_pics("images/towers/", str(self.stats['sprite_base'][0]))
        self.spriteGun = load_pics("images/towers/", str(self.stats['sprite_turret'][0]))
        self.spriteProj = load_pics("images/projectiles/", str(self.stats['sprite_proj'][0]))
        self.hitSound = pygame.mixer.Sound("sounds/game/" + str(self.stats['hit_sound'][0]) + ".wav")
        self.rotSpriteGun = self.spriteGun.copy()
        self.canFire = False

        # update all stats to match da level one
        self.update_stats(self.initialUpCost, self.upCostInc, self.curLevel,
                          self.dmgLevel[0], self.rateLevel[0], self.rangeLevel[0], self.specialLevel[0])
        self.placed = False  # becomes true after the tower is placed down
        self.pos = [0, 0]
        tar = []  # targetting purposes

    def upgrade_preview(self, stat_num):
        # damage
        if stat_num == 0:
            return int(self.stats['damage'][self.dmgLevel[0]]) - self.damage
        # rate
        if stat_num == 1:
            return (int(float(self.stats['rate'][self.rateLevel[0]]) * 100 - self.rate * 100)) / 100
        # range
        if stat_num == 2:
            return (int(float(self.stats['range'][self.rangeLevel[0]]) * 100 - self.range * 100)) / 100
        # special
        if stat_num == 3:
            return (int(float(self.stats['special_val'][self.specialLevel[0]]) * 100 - self.specialVal * 100)) / 100

    def update_stats(self, init_up, inc_up, cur_level, dmgl, ratel, rangel, specl):
        # final upgrade cost = initial cost + (increase * (level - 1))
        self.finalUpCost = int(init_up + inc_up * (cur_level - 1))
        self.damage = int(self.stats['damage'][dmgl - 1] * (1 + self.dmgBoost))
        self.rate = float(self.stats['rate'][ratel - 1] * (1 + self.rateBoost))
        self.range = float(self.stats['range'][rangel - 1] * (1 + self.rangeBoost))
        self.projSpd = float(self.stats['proj_spd'][rangel - 1] * (1 + self.projBoost))
        self.specialVal = float(self.stats['special_val'][specl - 1])
        if 'special_val2' in self.stats:  # 2nd special value upgrade
            self.specialVal2 = float(self.stats['special_val2'][specl - 1])

    def calc_boost(self, adj_tower_list):
        self.dmgBoost = 0
        self.rateBoost = 0
        self.rangeBoost = 0
        self.projBoost = 0

    def upgrade(self, stat_num):
        # update selling price (1/2 of tower cost + all upgrades)
        self.sellPrice += self.finalUpCost / 2
        # increment level and stuffs asdf
        self.curLevel += 1
        if stat_num == 0:
            self.dmgLevel[0] += 1
        elif stat_num == 1:
            self.rateLevel[0] += 1
        elif stat_num == 2:
            self.rangeLevel[0] += 1
        elif stat_num == 3:
            self.specialLevel[0] += 1

        self.update_stats(self.initialUpCost, self.upCostInc, self.curLevel,
                          self.dmgLevel[0], self.rateLevel[0], self.rangeLevel[0], self.specialLevel[0])

    # rotate the gun
    def rotate(self, angle):
        self.rotation = math.radians(angle)
        self.rotSpriteGun = components.rot_center(self.spriteGun, angle)

    # search for first enemy and rotate gun to face it
    def calc_rotation(self, enemy_pos, enemy_path_left, enemy_radius, dt):
        self.canFire = False
        tar = []
        path_left_cur = 1000

        for i in range(len(enemy_path_left)):
            dist_to_enemy = math.sqrt(((self.pos[0] * 50 - 25) - enemy_pos[i][0]) ** 2 +
                                      ((self.pos[1] * 50 - 25) - enemy_pos[i][1]) ** 2)
            # if the enemy is closer to the destination and within range, choose it as target
            if enemy_path_left[i] < path_left_cur and dist_to_enemy <= self.range * 50 + float(enemy_radius[i]) * 0.7:
                tar = [enemy_pos[i][0], enemy_pos[i][1]]
                path_left_cur = enemy_path_left[i]

        # tick down reload
        if self.reload > 0:
            self.reload -= dt
        elif tar != []:  # lets the main.py know this tower is ready
            self.canFire = True

        # trig :D
        if tar != []:
            diff = [tar[0] - (self.pos[0] * 50 - 25), tar[1] - (self.pos[1] * 50 - 25)]
            self.rotation = math.atan2(-diff[1], diff[0])
        self.rotSpriteGun = components.rot_center(self.spriteGun, math.degrees(self.rotation))

    # creates a projectile class based on tower params
    def fire_projectile(self):
        self.reload += (1 / self.rate) - 0.016
        tempSpecial = []  # now u can add extra special stuff
        if self.reload <= 0:
            self.canFire = True

        # pass special values to shot
        if self.special == "AOEslow":
            tempSpecial = [self.special, self.range, self.specialVal, self.specialVal2]
        else:
            tempSpecial = [self.special, self.specialVal]

        self.canFire = False
        xy_vel = [self.projSpd * math.cos(self.rotation) * 50, self.projSpd * -math.sin(self.rotation) * 50]
        temp_spr = components.rot_center(self.spriteProj, math.degrees(self.rotation))
        return projectile.Projectile([self.pos[0] * 50 - 25, self.pos[1] * 50 - 25], xy_vel,
                                     self.damage, self.range * self.effRange * 50, tempSpecial,
                                     temp_spr, str(self.stats['sprite_proj'][0]), self.hitSound)

    # draws a full turret, centered on a xy coordinate. The first picture is assumed to be the base.
    # rotation is an angle in radians that the turret should rotate
    def draw_tower_gun(self, display, xy):
        # draw gun
        temp = self.rotSpriteGun.get_rect()
        display.blit(self.rotSpriteGun, (xy[0] - temp[2] // 2, xy[1] - temp[3] // 2))

    # draw the base of a tower only
    def draw_tower_base(self, display, xy):
        # draw base
        temp = self.spriteBase.get_rect()
        display.blit(self.spriteBase, (xy[0] - temp[2] // 2, xy[1] - temp[3] // 2))

    # combines draw_tower_gun and draw_tower_base methods
    def draw_tower_full(self, display, xy):
        self.draw_tower_base(display, xy)
        self.draw_tower_gun(display, xy)

    # draws a range around the tower
    def draw_range(self, display, valid, xy=0):
        # colours
        col_range_valid = [120, 140, 140, 20]
        col_range_valid_outline = [50, 50, 50, 225]
        col_range_invalid = [200, 25, 25, 35]
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
