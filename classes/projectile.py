import pygame
import math

class Projectile(object):
    def __init__(self, xy, vel_xy, damage, range, special, sprite, exp, sound):
        self.posXYPx = xy
        self.vel = vel_xy
        self.totalVel = math.sqrt(vel_xy[0] ** 2 + vel_xy[1] ** 2)
        self.damage = damage
        self.distance = [0, range]  # current traveled, max
        self.special = special
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(sprite, 6)
        self.size = sprite.get_size()
        self.rectPos = [self.posXYPx[0] - self.size[0] / 2, self.posXYPx[1] - self.size[1]]  # top left corner pos
        self.exp = exp + "-hit"
        self.sound = sound

    # updates the projectile and then returns a list of enemies hit (can be multiple if the projectile is exploding
    def update(self, time, display, enemies):
        collided = []
        # check every 10 spaces for stuffs
        num_intervals = int(self.totalVel * time / 10) + 1
        time /= num_intervals
        for i in range(num_intervals):
            # move self (avg 10 tiles)
            self.posXYPx[0] += self.vel[0] * time
            self.posXYPx[1] += self.vel[1] * time
            self.rectPos = [self.posXYPx[0] - self.size[0] / 2, self.posXYPx[1] - self.size[1] / 2]
            self.distance[0] += math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2) * time

            # check collision or out of bounds
            for j in range(len(enemies)):
                diff = [int(self.rectPos[0] - enemies[j].posPx[0]), int(self.rectPos[1] - enemies[j].posPx[1])]
                if self.mask.overlap(enemies[j].mask, diff) is not None:
                    # draw sprite one last time before removal
                    display.blit(self.sprite,
                                 (int(self.posXYPx[0] - self.size[0] / 2), int(self.posXYPx[1] - self.size[1] / 2)))
                    # explosion
                    if self.special[0] == 'splash':
                        for k in range(len(enemies)):
                            aoe = float(self.special[1]) * 50
                            dist = math.sqrt((self.posXYPx[0] - enemies[k].posPx[0]) ** 2 +
                                             (self.posXYPx[1] - enemies[k].posPx[1]) ** 2)
                            if dist < aoe + int(enemies[k].stats['radius']) / 2:
                                collided.append(enemies[k])
                        return collided

                    else:  # normal hit
                        collided.append(enemies[j])
                        return collided

        # update image
        display.blit(self.sprite, (int(self.posXYPx[0] - self.size[0] / 2), int(self.posXYPx[1] - self.size[1] / 2)))

        return collided
