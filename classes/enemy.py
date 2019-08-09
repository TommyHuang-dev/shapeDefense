import pygame

# holds info about enemies, like hp and speed
class Enemy(object):
    def __init__(self, attributes, spawnpoint, spawn_num, hp_bonus, speed_bonus, regen_bonus, armour_bonus, bounty_bonus):
        # stats
        self.stats = attributes  # dict. of all stats
        self.mask = pygame.mask.from_surface(self.stats['sprite'], 24)
        self.status = []  # list of status effects like slow
        
        # set enemy stats and apply bonuses
        self.maxHP = int(int(self.stats['health']) * (1 + hp_bonus))
        self.curHP = self.maxHP
        self.speed = float(self.stats['speed']) * (1 + speed_bonus)
        self.regen = float(self.stats['regen']) * (1 + regen_bonus)
        self.armour = round(int(self.stats['armour']) * (1 + armour_bonus), 0)
        self.bounty = round(int(self.stats['bounty']) * (1 + bounty_bonus), 0)
        if 'special' in self.stats:
            self.special = self.stats['special']

        # pathing
        self.path_number = spawn_num
        self.movement_dir = [0, 0]
        self.direction_delay = -1
        self.endTimer = 0.1
        self.distance = 1000  # distance from end

        # positional (Px = pixel)
        self.tileLoc = spawnpoint
        self.posPx = [spawnpoint[0] * 50 - 25, spawnpoint[1] * 50 - 25]
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
        self.calc_tile_loc(self.posPx)
        if self.reachedEnd:
            self.endTimer -= time
        elif self.tileLoc == path[-1]:
            self.reachedEnd = True
            self.endTimer = 0.25
        else:
            self.distance = len(path) - path.index(self.tileLoc)

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

        # delay to center the enemy and not immediately change direction
        self.direction_delay -= time * temp_speed

        # regen hp
        if self.curHP < self.maxHP:
            self.curHP += self.regen * time * slow_regen_multi
        else:
            self.curHP = self.maxHP

        # recalculate pathing after the delay
        if not self.reachedEnd and self.direction_delay <= 0:
            cur_tile = path.index(self.tileLoc)
            # difference between current tile and target tile
            self.movement_dir = [self.tileLoc[0] - path[cur_tile + 1][0], self.tileLoc[1] - path[cur_tile + 1][1]]

        self.posPx[0] -= self.movement_dir[0] * time * temp_speed * 50
        self.posPx[1] -= self.movement_dir[1] * time * temp_speed * 50

    # inflicts damage after armour and stuffs. Special is used for specialy applied effects from the hit.
    def inflict_damage(self, damage, specials):
        if damage > self.armour:
            self.curHP -= damage - self.armour
        elif damage > 0:  # minimum of 1 damage each hit if the attack deals damage
            self.curHP -= 1
        if specials[0] != 'none':
            self.status.append([specials[0], specials[1], specials[2]])  # name, magnitude, duration

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
