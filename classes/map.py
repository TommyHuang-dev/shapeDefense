from functions import mapParse
import pygame


class Map(object):
    def __init__(self, name):
        info = mapParse.parse_coords(name)  # get the map info
        # set colours
        self.mapName = info[0][0]
        self.colBackground = [int(x) for x in info[0][1]]
        self.colObs = [int(x) for x in info[0][2]]
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

    def calc_valid(self, xy):
        for i in range(len(self.obsPxList)):
            if self.obsPxList[i].collidepoint(xy):
                return False

        return True

    # TODO: clean up the draw_preview code
    # draws a mini preview of the map
    def draw_preview(self, display, x, y, scale):
        # draw background
        pygame.draw.rect(display, self.colBackground, (x, y, 1000 * scale, 750 * scale))
        prev_obs_list = [x.fit((x[0] * scale, x[1] * scale, x[2] * scale, x[3] * scale)) for x in self.obsPxList]
        # preview obstacles
        for i in range(len(self.obsPxList)):
            pygame.draw.rect(display, self.colObs, (prev_obs_list[i][0] + x, prev_obs_list[i][1] + y,
                                                    prev_obs_list[i][2], prev_obs_list[i][3]))

        # preview spawn points and exit
        s_list = [[int(i[0] * 50 * scale - 50 * scale + x), int(i[1] * 50 * scale - 50 * scale + y)]
                  for i in self.spawnList]
        e_list = [[int(i[0] * 50 * scale - 50 * scale + x), int(i[1] * 50 * scale - 50 * scale + y)]
                  for i in self.exitList]
        for i in range(len(self.spawnList)):
            # make sure it doesnt go out of bounds
            if s_list[i][0] - x > 975 * scale:
                s_list[i][0] = 950 * scale + x + 25 * scale
            elif s_list[i][1] - y > 725 * scale:
                s_list[i][1] = 700 * scale + y + 25 * scale
            elif s_list[i][0] - x < 0 * scale:
                s_list[i][0] = -25 * scale + x
            elif s_list[i][1] - y < 0 * scale:
                s_list[i][1] = -25 * scale + y
            if e_list[i][0] - x > 975 * scale:
                e_list[i][0] = 950 * scale + x + 25 * scale
            elif e_list[i][1] - y > 725 * scale:
                e_list[i][1] = 700 * scale + y + 25 * scale
            elif e_list[i][0] - x < 0 * scale:
                e_list[i][0] = -25 * scale + x
            elif e_list[i][1] - y < 0 * scale:
                e_list[i][1] = -25 * scale + y

            # draw da rectangle
            pygame.draw.rect(display, (50, 225, 50), (s_list[i][0], s_list[i][1], 50 * scale, 50 * scale))
            pygame.draw.rect(display, (225, 50, 50), (e_list[i][0], e_list[i][1], 50 * scale, 50 * scale))

        # cover up the boxes
        pygame.draw.rect(display, (200, 225, 255), (x - 13, y - 13, 1000 * scale + 26, 750 * scale + 26), 26)
