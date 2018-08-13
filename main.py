from classes import tower
import mapParse
import data
import pygame
from pygame import gfxdraw
import math
import sys
import random
import time

# This is a simple tower defence, written in Python
# It may be moved into unity later
# Made by Tommy H
# Project started 2018-08-12


# this method draws a grid!!
# border draws a border around the grid, of the same colour as the grid itself
# offset offsets the lines drawn in the grid, negative values are recommended, default 0
def draw_grid(start_x, start_y, l, h, space, col, border, offset_l=0, offset_h=0, ):
    if l < 0 or h < 0 or space < 0:
        raise ValueError('draw_grid was called with less than 0 for length, height, or spacing!')

    end_x = start_x + l
    end_y = start_y + h
    # vertical lines
    for i in range((l - 1 - offset_l) // space):
        pygame.draw.line(screen, col, (start_x + offset_l + (i + 1) * space, start_y),
                         (start_x + offset_l + (i + 1) * space, end_y - 1))
    # horizontal lines
    for i in range((h - 1 - offset_h) // space):
        pygame.draw.line(screen, col, (start_x, start_y + offset_h + (i + 1) * space),
                         (end_x - 1, start_y + offset_h + (i + 1) * space,))
    # border
    if border:
        pygame.draw.rect(screen, col, (start_x, start_y, l, h), 1)


# draws the path based on a list of corners, uses lines for the path, circles to fill in corners
def draw_path(corner_list, col):
    pygame.draw.lines(screen, col, False, corner_list, 45)
    for i in range(len(corner_list)):
        pygame.gfxdraw.filled_circle(screen, corner_list[i][0], corner_list[i][1], 22, col)


# ---- SETUP (only ran once) ----
# setup pygame
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
time.sleep(0.5)

# setup display and clock
clock = pygame.time.Clock()
disLength = 1300  # right 300 used for buying stuff and menu
disHeight = 750  # all 750 used for the map (1000 x 750 = 20 x 15 tiles)
screen = pygame.display.set_mode((disLength, disHeight))
pygame.display.set_caption("Shape Defense")

# ---- POST-SETUP (ran as the outer loop) ----
# - MAP STUFF -
# available and selected map info (difficulty, colours, corner)
mapList = ["easy, med, hard"]
selectedMap = ["med"]
pathCorners = mapParse.parseCoords("med")
# convert grid info to pixel coords
pathCoords = []
for i in range(3, len(pathCorners), 1):
    pathCoords.append([pathCorners[i][0] * 50 - 25, pathCorners[i][1] * 50 - 25])

# change score multiplier based on first pathCorners value (the map difficulty)
# easy = 0.75x, med = 1x, hard = 1.25x
scoreMulti = (pathCorners[0] + 2) / 4
print("score multiplier: ", scoreMulti)

# colours, grass, path, and grid colours are based off the map file
colGrass = pathCorners[1]
colPath = pathCorners[2]
colGrid = [colGrass[0] - 10, colGrass[1] - 30, colGrass[2] + 10]
colPurchaseMenu = [160, 190, 240]

# delete unnecessary path corners info
del(pathCorners[0])
del(pathCorners[1])
del(pathCorners[2])

# ---- IN-GAME ----
while True:
    # ---- BACKGROUND ----
    screen.fill(colGrass)
    draw_grid(0, 0, disLength - 300, disHeight, 50, colGrid, False)
    draw_path(pathCoords, colPath)

    # ---- UI ELEMENTS ----

    # ui background and borders
    pygame.draw.rect(screen, colPurchaseMenu, (disLength - 300, 0, 300, disHeight), 0)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, disLength, disHeight), 3)
    pygame.draw.line(screen, (0, 0, 0), (disLength - 300, 0), (disLength - 300, disHeight), 3)

    # update display!
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()