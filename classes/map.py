from functions import mapParse
import pygame

class Map():
    def __init__(self, name):
        info = mapParse.parse_coords(name)  # get the map info
        # set colours
        self.colBackground = [int(x) for x in info[0][0]]
        self.colObs = [int(x) for x in info[0][1]]
        self.colGrid = [x - 20 for x in self.colBackground]

        # set spawn, exit, and obstacle lists
        self.spawnList = []
        self.exitList = []  # matching exit to the spawnList
        self.obsList = []
        self.obsPxList = []
        for i in range(len(info[1])):
            self.spawnList.append([int(info[1][i][0]), int(info[1][i][1])])
            self.exitList.append([int(info[1][i][2]), int(info[1][i][3])])
        for i in range(len(info[2])):  # split the list into a list and rect object
            # this list is based on the 20x15 grid
            self.obsList.append([int(info[2][i][0]), int(info[2][i][1]),
                                 int(info[2][i][2]), int(info[2][i][3])])
            # this is based on the pixel values, rect object
            self.obsPxList.append(pygame.Rect(int(info[2][i][0]) * 50 - 50, int(info[2][i][1]) * 50 - 50,
                                              int(info[2][i][2]) * 50, int(info[2][i][3]) * 50))

    # draws.. obstacles
    def draw_obstacles(self, display):
        for i in range(len(self.obsPxList)):
            pygame.draw.rect(display, self.colObs, self.obsPxList[i])

    # draws a mini preview of the map
    def draw_preview(self, display, x, y, scale):
        # draw background
        pygame.draw.rect(display, self.colBackground, (x, y, 1000 * scale, 750 * scale))
        preview_obs_list = [x.fit((x[0] * scale, x[1] * scale, x[2] * scale, x[3] * scale)) for x in self.obsPxList]
        # preview obstacles
        for i in range(len(self.obsPxList)):
            pygame.draw.rect(display, self.colObs, (preview_obs_list[i][0] + x, preview_obs_list[i][1] + y,
                                                    preview_obs_list[i][2], preview_obs_list[i][3]))

