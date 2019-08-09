from classes import enemy


class Spawner(object):
    def __init__(self, attributes, enemy_attributes, level):
        self.name = attributes[0]
        self.interval = attributes[3]
        self.amount = attributes[1]
        self.timer = self.interval - 0.25
        self.spawned_enemy = enemy_attributes

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

    def spawn_enemy(self, spawnpoint, spawn_num):
        enemy_obj = enemy.Enemy(self.spawned_enemy, spawnpoint, spawn_num, 
                self.hp_bonus, self.speed_bonus, self.regen_bonus, self.armour_bonus, self.bounty_bonus)
        self.amount -= 1
        return enemy_obj
