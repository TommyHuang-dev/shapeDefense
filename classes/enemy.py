import pygame

# holds info about enemies, like hp and speed
class Enemy(object):
    def __init__(self, attributes, spawnpoint, spawn_num, level):
        # stats
        self.stats = attributes  # dict. of all stats
        self.mask = pygame.mask.from_surface(self.stats['sprite'], 24)
        self.status = []  # list of status effects like slow

        # convert attributes to stats
        # increase HP based on wave (+10%) for < 25, (+15%) for 25 < x <= 50, (+20%) for x > 50
        self.maxHP = int(int(self.stats['health']) * (1 + level * 0.1))
        if level > 25:
            # increase 5% again
            self.maxHP += int(int(self.stats['health']) * (1 + (level - 25) * 0.05))
        if level > 50:
            # increase 5% AGAIN
            self.maxHP += int(int(self.stats['health']) * (1 + (level - 50) * 0.05))

        self.curHP = self.maxHP
        # following stats max out at level 50
        if level > 50:
            level = 50
        self.speed = float(self.stats['speed']) * (1 + level * 0.01)
        self.armour = int(int(self.stats['armour']) * (1 + level * 0.04))
        self.regeneration = float(self.stats['regeneration']) * (1 + level * 0.05)
        self.bounty = int(int(self.stats['bounty']) * (1 + level * 0.02))

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
            self.direction_delay = 0.5

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
        biggest_slow = 0
        i = 0
        while i < len(self.status):
            if 'slow' in self.status[i]:  # slowed
                if self.status[i][1] > biggest_slow:
                    biggest_slow = self.status[i][1]
                self.status[i][2] -= time  # reduce slow timer, delete status effect after it runs out
                if self.status[i][2] <= 0:
                    del self.status[i]
                    i -= 1
                i += 1
        slow_regen_multi = 1 - biggest_slow
        # bosses are less affected by slow, but fully affected by the HP regen reduction
        if self.stats['type'] == 'BOSS':
            biggest_slow /= 2
        temp_speed *= (1 - biggest_slow)  # apply slow

        # delay to center the enemy and not immediately change direction
        self.direction_delay -= time * temp_speed

        # regeneration
        if self.curHP < self.maxHP:
            self.curHP += self.regeneration * time * slow_regen_multi
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
        if specials[0] == 'AOEslow':
            self.status.append(['slow', specials[2], specials[3]])  # name, magnitude, duration

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
