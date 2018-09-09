import pygame
import math

class Projectile(object):
    def __init__(self, xy, vel_xy, damage, range, special, sprite):
        self.posXYPx = xy
        self.vel = vel_xy
        self.damage = damage
        self.distance = [0, range]  # current traveled, max
        self.special = special
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(sprite, 1)
        self.size = sprite.get_size()
        self.rectPos = [self.posXYPx[0] - self.size[0] / 2, self.posXYPx[1] - self.size[1]]

    def update(self, display):
        self.posXYPx[0] += self.vel[0]
        self.posXYPx[1] += self.vel[1]
        self.rectPos = [self.posXYPx[0] - self.size[0] / 2, self.posXYPx[1] - self.size[1] / 2]
        self.distance[0] += math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
        display.blit(self.sprite, (int(self.posXYPx[0] - self.size[0] / 2), int(self.posXYPx[1] - self.size[1] / 2)))

