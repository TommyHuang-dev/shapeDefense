import pygame


# boom!!!
class Explosion(object):
    def __init__(self, xy, pictures):
        self.picList = pictures
        self.posXYPx = xy
        self.timer = 0.12
        self.curpic = 0
        self.stopped = False
        self.size = pictures[0].get_size()

    def show(self, display, dt):
        display.blit(self.picList[self.curpic], (self.posXYPx[0] - self.size[0] / 2, self.posXYPx[1] - self.size[1] / 2))
        self.timer -= dt
        if self.timer <= 0:
            self.timer = 0.15
            if self.curpic < len(self.picList) - 1:
                self.curpic += 1
            else:
                self.stopped = True
