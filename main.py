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
# music: main menu wii music!! ingame atlas plug
# easy: -10% speed on enemies, med: nothing, hard: +10% speed on enemies


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
menuScreenButtonFont = pygame.font.SysFont('Arial', 35,  False)
menuScreenHeaderFont = pygame.font.SysFont('Arial', 45,  True)
menuScreenHeaderFont.set_underline(True)  # sets underline for a font

# initialize maps
mapList = ["easy", "med", "hard"]  # map file names
mapNames = ["Breezy Meadows (easy)", "Meandering Forest (med)", "Blazing Desert (hard)"]  # map display names
selectedMap = "none"

# menu screen colours
colBackground = [200, 225, 255]

# list to hold rect objects and their colour
buttons = []
buttonsCol = []

# create list of buttons and their colour
for i in range(len(mapList)):
    colours = mapParse.parse_coords(mapList[i])
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
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disLength, disHeight), 2)

        # draw the buttons
        for i in range(len(buttons)):
            pygame.draw.rect(screen, buttonsCol[i], buttons[i])
            pygame.draw.rect(screen, (0, 0, 0), buttons[i], 1)
            components.create_text(screen, (buttons[i][0] + buttons[i][2] // 2, buttons[i][1] + buttons[i][3] // 2),
                                   mapNames[i], menuScreenButtonFont, (15, 15, 15))

        # draw prompt msg
        components.create_text(screen, (disLength // 2, 250),
                               "Choose a level", menuScreenHeaderFont, (0, 0, 0))

        # get mouse press on a button
        mousePos = pygame.mouse.get_pos()
        for i in range(len(buttons)):
            if buttons[i].collidepoint(mousePos):
                # on hover, draw thicker outline
                pygame.draw.rect(screen, (0, 0, 0), buttons[i], 3)
                # on click, set map and close out intro
                if pygame.mouse.get_pressed()[0] == 1:
                    selectedMap = mapList[i]
                    intro = False

        # title name
        screen.blit(titlePic, (0, 50))

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
        clock.tick(60)

    # ---- IN-GAME SETUP ----

    # get path for the selected map
    pathCorners = mapParse.parse_coords(selectedMap)
    obstacleLoc = mapParse.parse_obstacles(selectedMap)

    # convert grid info to pixel coords
    pathCoords = []
    obstacleCoords = []
    for i in range(3, len(pathCorners), 1):
        pathCoords.append([pathCorners[i][0] * 50 - 25, pathCorners[i][1] * 50 - 25])
    for i in range(1, len(obstacleLoc), 1):
        obstacleCoords.append([obstacleLoc[i][0] * 50 - 25, obstacleLoc[i][1] * 50 - 25])

    # change score multiplier based on first pathCorners value (the map difficulty)
    # easy = 0.75x, med = 1x, hard = 1.25x
    scoreMulti = (pathCorners[0] + 2) / 4
    print("score multiplier: ", scoreMulti)

    # Colours of various objects
    colGrass = pathCorners[1]
    colPath = pathCorners[2]
    colGrid = [colGrass[0] - 20, colGrass[1] - 20, colGrass[2] - 20]
    colPurchaseMenu = [200, 200, 220]
    colObs = obstacleLoc[0]

    # delete unnecessary path corners info
    del(pathCorners[0])
    del(pathCorners[1])
    del(pathCorners[2])
    del(obstacleLoc[0])

    # towers (turrets + boosters)
    towerList = ['placeholder']

    # tower buttons
    turretButtonList = [pygame.Rect(disLength - 200, 100, 100, 100), pygame.Rect(disLength - 200, 250, 100, 100)]
    boosterButtonList = []

    # placeholder tower
    basicTurretImg = load_pics("images/towers/", "basic")

    # ---- GAME LOOP ----
    while not intro:
        # ---- BACKGROUND ----
        screen.fill(colGrass)
        components.draw_grid(screen, 0, 0, disLength - 300, disHeight, 50, colGrid, False)
        components.draw_path(screen, pathCoords, colPath)
        # obstacles
        for i in range(len(obstacleLoc)):
            pygame.draw.circle(screen, colObs, (obstacleCoords[i][0], obstacleCoords[i][1]), 21)

        # ---- UI ELEMENTS ----
        # ui background and borders
        pygame.draw.rect(screen, colPurchaseMenu, (disLength - 300, 0, 300, disHeight), 0)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disLength, disHeight), 3)
        pygame.draw.line(screen, (0, 0, 0), (disLength - 300, 0), (disLength - 300, disHeight), 3)

        # purchase towers
        for i in range(len(turretButtonList)):
            pygame.draw.rect(screen, (50, 50, 50), (turretButtonList[i]), 2)
            screen.blit(pygame.transform.scale(basicTurretImg, (100, 100)), (disLength - 200, 100))
            screen.blit(pygame.transform.scale(basicTurretImg, (100, 100)), (disLength - 200, 250))

        for i in range(len(boosterButtonList)):
            pass
        # update display!
        pygame.display.update()

        # should make it 60FPS max
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()