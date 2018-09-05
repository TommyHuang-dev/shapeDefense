import random

class Enemy(object):
    def __init__(self, attributes, spawnpoint, spawn_num):
        # stats
        self.stats = attributes
        # pathing
        self.path_number = spawn_num
        self.movement_dir = [0, 0]
        self.direction_delay = -1
        self.endTimer = 0.1
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
            self.direction_delay = 0.5 * random.uniform(0.95, 1.05)

    # move tiles based on the pre-designated path
    def move(self, path, time):
        # delay to center the enemy and not immeadiately move
        self.direction_delay -= time * float(self.stats['speed'])

        self.calc_tile_loc(self.posPx)
        if self.reachedEnd:
            self.endTimer -= time
        elif self.tileLoc == path[-1]:
            self.reachedEnd = True
            self.endTimer = 0.25

        # recalculate pathing after the delay
        cur_tile = path.index(self.tileLoc)
        if not self.reachedEnd and self.direction_delay <= 0:
            # difference between current tile and target tile
            self.movement_dir = [self.tileLoc[0] - path[cur_tile + 1][0], self.tileLoc[1] - path[cur_tile + 1][1]]

        self.posPx[0] -= self.movement_dir[0] * time * float(self.stats['speed']) * 50
        self.posPx[1] -= self.movement_dir[1] * time * float(self.stats['speed']) * 50


