from classes import enemy

class Spawner(object):
    def __init__(self, attributes, enemy_attributes):
        self.name = attributes[0]
        self.interval = attributes[3]
        self.amount = attributes[1]
        self.timer = 0
        self.spawned_enemy = enemy_attributes

    def spawn_enemy(self, spawnpoint, spawn_num):
        enemy_obj = enemy.Enemy(self.spawned_enemy, spawnpoint, spawn_num)
        return enemy_obj
