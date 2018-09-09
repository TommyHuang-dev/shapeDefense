import pygame

# holds info about enemies, like hp and speed
class Enemy(object):
    def __init__(self, attributes, spawnpoint, spawn_num, level):
        # stats
        self.stats = attributes
        self.mask = pygame.mask.from_surface(self.stats['sprite'], 24)
        self.status = []  # list of status effects like slow

        # convert attributes to stats
        # increase HP based on wave (+10%)
        self.maxHP = int(int(self.stats['health']) * (1 + level / 10))
        self.curHP = self.maxHP
        # following stats max out at level 50
        if level > 50:
            level = 50
        self.speed = float(self.stats['speed']) * (1 + level / 100)
        self.armour = int(int(self.stats['armour']) * (1 + level / 50))
        self.regeneration = float(self.stats['regeneration']) * (1 + level / 25)
        self.bounty = int(int(self.stats['bounty']) * (1 + level / 50))

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

    # calculate tile pos. based on pixel coordinate
    def calc_tile_loc(self, pos):
        prevLoc = self.tileLoc
        self.tileLoc = [pos[0] // 50 + 1, pos[1] // 50 + 1]
        # change direction delay if the new tile is different
        if prevLoc != self.tileLoc:
            self.direction_delay = 0.5 - self.speed / 120

    # move tiles based on the pre-designated path
    def move(self, path, time):
        # delay to center the enemy and not immeadiately move
        self.direction_delay -= time * self.speed
        self.calc_tile_loc(self.posPx)
        if self.reachedEnd:
            self.endTimer -= time
        elif self.tileLoc == path[-1]:
            self.reachedEnd = True
            self.endTimer = 0.25
        else:
            self.distance = len(path) - path.index(self.tileLoc)

        # regeneration
        if self.curHP < self.maxHP:
            self.curHP += self.regeneration * time
        else:
            self.curHP = self.maxHP

        # recalculate pathing after the delay
        if not self.reachedEnd and self.direction_delay <= 0:
            cur_tile = path.index(self.tileLoc)
            # difference between current tile and target tile
            self.movement_dir = [self.tileLoc[0] - path[cur_tile + 1][0], self.tileLoc[1] - path[cur_tile + 1][1]]

        self.posPx[0] -= self.movement_dir[0] * time * self.speed * 50
        self.posPx[1] -= self.movement_dir[1] * time * self.speed * 50

    # draw da hp bar and armour symbol
    def draw_bar(self, display):
        if self.curHP < self.maxHP:
            hp_perc = self.curHP / self.maxHP
            if self.stats['type'] == 'BOSS':
                pygame.draw.rect(display, (0, 0, 0), (self.posPx[0] - 30, self.posPx[1] - self.stats['radius'] - 12,
                                                      60, 8), 1)
                pygame.draw.rect(display, (250, 25, 25), (self.posPx[0] - 29, self.posPx[1] - self.stats['radius'] - 11,
                                                      58 * hp_perc, 6))

            else:
                pygame.draw.rect(display, (0, 0, 0), (self.posPx[0] - 20, self.posPx[1] - int(self.stats['radius']) - 8,
                                                      40, 6), 1)
                pygame.draw.rect(display, (250, 25, 25), (self.posPx[0] - 19,
                                                          self.posPx[1] - int(self.stats['radius']) - 7,
                                                          38 * hp_perc, 4))
