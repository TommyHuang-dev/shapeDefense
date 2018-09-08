import pygame


# boom!!!
class Explosion(object):
    def __init__(self, xy, pictures):
        self.picList = pictures
        self.posXYPx = xy
        self.timer = 0.1
        self.stopped = False

    def show(self, display, dt):
        display.blit(self.picList[0], self.posXYPx)
        self.timer -= dt
        if self.timer <= 0:
            self.timer = 0.1
            if len(self.picList) > 1:
                del(self.picList[0])
            else:
                self.stopped = True
