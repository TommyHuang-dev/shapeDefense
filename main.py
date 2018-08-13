from classes import tower
import data
import pygame
import math
import sys
import random
import time

# This is a simple tower defence, written in Python
# It may be moved into unity later
# Made by Tommy H
# Project started 2018-08-12


# this method draws a grid!!
# stx = starting x value, sty = starting y value
# l and h are length and height (going right and down), space is spacing between lines
# col is colour based on the 0-255 RGB scale.
# border draws a border around the grid, of the same colour as the grid itself
# offset offsets the lines drawn in the grid, negative values are recommended, default 0
def draw_grid(stx, sty, l, h, space, col, border, offset_l=0, offset_h=0,):
    if l < 0 or h < 0 or space < 0:
        raise ValueError('draw_grid was called with less than 0 for length, height, or spacing!')

    end_x = stx + l
    end_y = sty + h
    # vertical lines
    for i in range((l - 1 - offset_l) // space):
        pygame.draw.line(screen, col, (stx + offset_l + (i + 1) * space, sty),
                         (stx + offset_l + (i + 1) * space, end_y - 1))
    # horizontal lines
    for i in range((h - 1 - offset_h) // space):
        pygame.draw.line(screen, col, (stx, sty + offset_h + (i + 1) * space),
                         (end_x - 1, sty + offset_h + (i + 1) * space,))

    if border:
        pygame.draw.rect(screen, col, (stx, sty, l, h), 1)

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

# colours
screenCol = [150, 250, 150]
purchaseMenuCol = [120, 140, 200]
gridCol = [140, 220, 160]


while True:
    # draw background
    screen.fill(screenCol)
    draw_grid(0, 0, disLength - 300, disHeight, 50, gridCol, False)

    # draw UI and menu elements
    pygame.draw.rect(screen, purchaseMenuCol, (disLength - 300, 0, 300, disHeight), 0)
    pygame.draw.line(screen, (0, 0, 0), (disLength - 300, 0), (disLength - 300, disHeight), 2)

    # update display!
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


