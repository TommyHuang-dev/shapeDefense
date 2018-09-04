
class Enemy(object):
    def __init__(self, attributes, spawnpoint, spawn_num):
        # stats
        self.stats = attributes
        # pathing
        self.path_number = spawn_num
        # positional (Px = pixel)
        self.tileLoc = spawnpoint
        self.posPx = [spawnpoint[0] * 50 - 25, spawnpoint[1] * 50 - 25]

    def calc_tile_loc(self, pos):
        self.tileLoc = [pos[0] // 50 + 1, pos[1] // 50 + 1]

    def move(self, path):
        self.calc_tile_loc(self.posPx)