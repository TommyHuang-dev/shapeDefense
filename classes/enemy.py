import pygame
import math
import random
import functions.components

# holds info about enemies, like hp and speed
class Enemy(object):
    def __init__(self, attributes, spawnpoint, spawn_num, level):
        # stats
        self.stats = attributes  # dict. of all stats
        self.sprite = self.stats['sprite']
        self.mask = pygame.mask.from_surface(self.stats['sprite'], 24)
        self.status = []  # list of status effects like slow
        self.movetype = self.stats['movement_type']
        
        # enemy % bonuses based on level
        # no scaling limit
        # hp bonus: arithmetic series
        # increases at a base rate of 10% per wave. Rate increases by 1% (+10%, +11%, +12%...). Bonus +30% after level 50
        # lvl 10: 250% hp
        # lvl 30: 850% hp
        # lvl 50: 1850% hp
        # lvl 70: 3250% hp
        self.hp_bonus = level * (0.095 + level * 0.005)
        
        # other stat bonuses stops at lvl 50. But rate of health scaling is increased.
        if level > 50:
            self.hp_bonus += (level - 50) * (0.3)
            level = 50
        self.speed_bonus = 0.008 * level  # max +40% (1.5x)
        # regen bonus: increases at base rate of +4%. Rate increases after level 20 and level 40
        self.regen_bonus = level * (0.05)  # max + 540% (6.4x)
        if level > 20:
            self.regen_bonus += (level - 20) * (0.07)
        if level > 40:
            self.regen_bonus += (level - 40) * (0.08)
        self.armour_bonus = 0.03 * level  # max +150% (2.5x)
        self.bounty_bonus = 0.04 * level  # max +200% (3x)

        # set enemy stats and apply bonuses
        self.maxHP = int(int(self.stats['health']) * (1 + self.hp_bonus))
        self.curHP = self.maxHP
        self.speed = float(self.stats['speed']) * (1 + self.speed_bonus)
        self.regen = float(self.stats['regen']) * (1 + self.regen_bonus)
        self.armour = round(int(self.stats['armour']) * (1 + self.armour_bonus), 0)
        self.bounty = round(int(self.stats['bounty']) * (1 + self.bounty_bonus), 0)
        if 'special' in self.stats:
            self.special = self.stats['special']

        self.dmg = int(self.stats['dmg'])  # amount of damage dealt to life
        
        # pathing
        self.path_number = spawn_num
        self.direction_delay = -1
        self.endTimer = 0.1

        self.movement_dir = [0, 0]
        self.distance = 1000  # distance from end
        self.radius = float(self.stats['radius'])
        if self.movetype == "AIR":
            self.recalcTimer = [0, 0.5]  # recalculate pathing 2 times per sec
            self.rotation = 0.0  # rotation in radians for air units

        # positional (Px = pixel)
        self.tileLoc = spawnpoint
        self.posPx = [spawnpoint[0] * 50 - 25 + random.uniform(-5, 5), spawnpoint[1] * 50 - 25 + random.uniform(-5, 5)]
        self.reachedEnd = False
        self.secSpawn = attributes['death_spawn_enemy']
        self.secValue = int(attributes['death_spawn_val'])

    # calculate tile pos. based on pixel coordinate
    def calc_tile_loc(self, pos):
        prevLoc = self.tileLoc
        self.tileLoc = [pos[0] // 50 + 1, pos[1] // 50 + 1]
        # change direction delay if the new tile is different
        if prevLoc != self.tileLoc:
            self.direction_delay = 0.45

    # move tiles based on the pre-designated path
    def move(self, path, time):
        # slows and other status effects
        temp_speed = self.speed
        slow_spd = 1.0
        i = 0
        while i < len(self.status):
            if 'slow' in self.status[i]:  # slowed
                # slows stack diminishingly
                slow_spd *= (1-self.status[i][1])
                
                self.status[i][2] -= time  # reduce slow timer, delete status effect after it runs out
                if self.status[i][2] <= 0:
                    del self.status[i]
                    i -= 1
                i += 1
        if slow_spd < 0:  # make sure enemies dont go backwards lol
            slow_spd = 0
        
        # bosses are less affected by slows
        if self.stats['type'] == 'BOSS':
            slow_spd += (1 - slow_spd) * 0.3
        
        slow_regen_multi = slow_spd  # regen reduction
        temp_speed *= slow_spd  # apply slow

        # regen hp
        if self.curHP < self.maxHP:
            self.curHP += self.regen * time * slow_regen_multi
        else:
            self.curHP = self.maxHP

        # land enemies
        if self.movetype == "GROUND":
            self.calc_tile_loc(self.posPx)
            if self.reachedEnd:
                self.endTimer -= time
            elif self.tileLoc == path[-1]:
                self.reachedEnd = True
                self.endTimer = 0.3
            else:
                self.distance = len(path) - path.index(self.tileLoc)

            # delay to center the enemy and not immediately change direction
            self.direction_delay -= time * temp_speed

            # recalculate pathing after the delay
            if not self.reachedEnd and self.direction_delay <= 0:
                cur_tile = path.index(self.tileLoc)
                # difference between current tile and target tile
                self.movement_dir = [self.tileLoc[0] - path[cur_tile + 1][0], self.tileLoc[1] - path[cur_tile + 1][1]]

            self.posPx[0] -= self.movement_dir[0] * time * temp_speed * 50
            self.posPx[1] -= self.movement_dir[1] * time * temp_speed * 50
        
        # flying enemies
        elif self.movetype == "AIR":
            self.recalcTimer[0] -= time

            self.calc_tile_loc(self.posPx)
            if self.reachedEnd:
                self.endTimer -= time
            elif self.tileLoc == path[-1]:
                self.reachedEnd = True
                self.endTimer = 0.3
            
            if self.recalcTimer[0] <= 0:  # simply find a straight path to da end
                self.movement_dir = [self.posPx[0] - path[-1][0] * 50 + 25, self.posPx[1] - path[-1][1] * 50 + 25]
                temp_total = math.sqrt(self.movement_dir[0] ** 2 + self.movement_dir[1] ** 2)  # pythagorean theorem dat shit
                self.movement_dir = [self.movement_dir[0] / temp_total, self.movement_dir[1] / temp_total]
                self.rotation = math.degrees(math.atan2(-self.movement_dir[1], self.movement_dir[0]) + math.pi)
                self.recalcTimer[0] = self.recalcTimer[1]
                self.distance = temp_total / 50  # distance! :D

                # rotating sprite
                # snap to 90 degree angles
                
                if self.rotation % 90 > 89 or self.rotation % 90 < 1:
                    self.rotation = round(self.rotation / 90) * 90

                self.rot_sprite = functions.components.rot_center(self.sprite, self.rotation)
            
            self.distance -= temp_speed * time
            self.posPx[0] -= self.movement_dir[0] * time * temp_speed * 50
            self.posPx[1] -= self.movement_dir[1] * time * temp_speed * 50

        else:
            print("enemy movement not defined")

    # inflicts damage after armour and stuffs. Special is used for specialy applied effects from the hit.
    def inflict_damage(self, damage, specials):
        # apply special effects
        if specials[0] == 'antiair':
            if self.movetype == "AIR":
                damage *= specials[1]
        elif specials[0] != 'none':
            self.status.append([specials[0], specials[1], specials[2]])  # name, magnitude, duration
        
        # deal damage
        if damage - self.armour >= 1:
            self.curHP -= damage - self.armour
        elif damage > 0:  # minimum of 0.5 damage each hit if the attack deals damage
            self.curHP -= 0.5

    # draw da hp bar and armour symbol
    def draw_bar(self, display, a_pic):
        #hp bar
        if self.curHP < self.maxHP:
            hp_perc = self.curHP / self.maxHP
            if self.stats['type'] == 'BOSS':
                pygame.draw.rect(display, (0, 0, 0), (self.posPx[0] - 30, self.posPx[1] - int(self.stats['radius']) - 12,
                                                      60, 8), 1)
                pygame.draw.rect(display, (250, 25, 25), (self.posPx[0] - 29, self.posPx[1] - int(self.stats['radius']) - 11,
                                                      58 * hp_perc, 6))

            else:
                pygame.draw.rect(display, (0, 0, 0), (self.posPx[0] - 20, self.posPx[1] - int(self.stats['radius']) - 8,
                                                      40, 6), 1)
                pygame.draw.rect(display, (250, 25, 25), (self.posPx[0] - 19,
                                                          self.posPx[1] - int(self.stats['radius']) - 7,
                                                          38 * hp_perc, 4))

        # armour
        if self.armour > 0:
            if self.stats['type'] == 'BOSS':
                display.blit(a_pic, (self.posPx[0] - 6, self.posPx[1] - 44))
            else:
                display.blit(a_pic, (self.posPx[0] - 6, self.posPx[1] - 34))
