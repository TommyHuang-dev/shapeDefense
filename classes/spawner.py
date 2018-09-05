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
        self.amount -= 1
        return enemy_obj
