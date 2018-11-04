import pygame


# boom!!!
class Explosion(object):
    def __init__(self, xy, pictures, scaling):
        self.picList = pictures.copy()
        # rescale image size for splash towers
        self.scale = int(scaling)
        if self.scale != -1:
            for i in range(len(self.picList)):
                self.picList[i] = pygame.transform.scale(self.picList[i], (self.scale, self.scale))
        self.posXYPx = xy
        self.timer = 0.1
        self.curpic = 0
        self.stopped = False
        self.size = self.picList[0].get_size()

    def show(self, display, dt):
        display.blit(self.picList[self.curpic], (self.posXYPx[0] - self.size[0] / 2, self.posXYPx[1] - self.size[1] / 2))
        self.timer -= dt
        if self.timer <= 0:
            self.timer = 0.15
            if self.curpic < len(self.picList) - 1:
                self.curpic += 1
            else:
                self.stopped = True
