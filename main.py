from functions import mapParse
from functions import components
import savefiles
import classes
import data
import sounds
import time
import pygame
from pygame import gfxdraw
import sys

def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


# This is a simple tower defence, written in Python
# It may be moved into unity later
# Made by Tommy H
# Project started 2018-08-12

# ---- SETUP (only ran once) ----
# setup pygame
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.font.init()
pygame.mixer.init()
time.sleep(0.5)

# setup display and clock
clock = pygame.time.Clock()
disLength = 1300  # right 300 used for buying stuff and menu
disHeight = 750  # all 750 used for the map (1000 x 750 = 20 x 15 tiles)
screen = pygame.display.set_mode((disLength, disHeight))
pygame.display.set_caption("Shape Defense")

intro = True

# font stuff
menuScreenButtonFont = pygame.font.SysFont('Arial', 35,  True)
menuScreenHeaderFont = pygame.font.SysFont('Arial', 45,  True)
menuScreenHeaderFont.set_underline(True)  # sets underline for a font

# initialize maps
mapList = ["easy", "med", "hard"]
mapNames = ["Breezy Meadows", "Windy Forest", "Blazing Desert"]
selectedMap = "none"

# menu screen colours
colBackground = [200, 225, 255]

# list to hold rect objects and their colour
buttons = []
buttonsCol = []

# create list of buttons and their colour
for i in range(len(mapList)):
    colours = mapParse.parseCoords(mapList[i])
    buttonsCol.append(colours[1])
    buttons.append(pygame.Rect(400, 300 + i * 125, 500, 100))

# load hardcoded images
titlePic = load_pics("images/UI/", "title")

# ---- OUTER LOOP ----
while True:
    # ---- INTRO SCREEN ----
    while intro:
        # background
        screen.fill(colBackground)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disLength, disHeight), 3)

        # draw the buttons
        for i in range(len(buttons)):
            pygame.draw.rect(screen, buttonsCol[i], buttons[i])
            pygame.draw.rect(screen, (0, 0, 0), buttons[i], 3)
            components.create_text(screen, (buttons[i][0] + buttons[i][2] // 2, buttons[i][1] + buttons[i][3] // 2),
                                   mapNames[i], menuScreenButtonFont, (15, 15, 15))

        # draw prompt msg
        components.create_text(screen, (disLength // 2, 250),
                               "Choose a level", menuScreenHeaderFont, (0, 0, 0))

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # get mouse press on a button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                for i in range(len(buttons)):
                    if buttons[i].collidepoint(mouse_pos):
                        # set map and close out intro
                        selectedMap = mapList[i]
                        intro = False

        # title name
        screen.blit(titlePic, (0, 50))

        pygame.display.update()
        clock.tick(60)

    # draws path for the selected map
    pathCorners = mapParse.parseCoords(selectedMap)
    # convert grid info to pixel coords
    pathCoords = []
    for i in range(3, len(pathCorners), 1):
        pathCoords.append([pathCorners[i][0] * 50 - 25, pathCorners[i][1] * 50 - 25])

    # change score multiplier based on first pathCorners value (the map difficulty)
    # easy = 0.75x, med = 1x, hard = 1.25x
    scoreMulti = (pathCorners[0] + 2) / 4
    print("score multiplier: ", scoreMulti)

    # Colours of various objects
    colGrass = pathCorners[1]
    colPath = pathCorners[2]
    colGrid = [colGrass[0] - 20, colGrass[1] - 20, colGrass[2] - 20]
    colPurchaseMenu = [190, 205, 240]

    # delete unnecessary path corners info
    del(pathCorners[0])
    del(pathCorners[1])
    del(pathCorners[2])

    # ---- IN-GAME ----
    while not intro:
        # ---- BACKGROUND ----
        screen.fill(colGrass)
        components.draw_grid(screen, 0, 0, disLength - 300, disHeight, 50, colGrid, False)
        components.draw_path(screen, pathCoords, colPath)

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