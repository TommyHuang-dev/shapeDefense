from functions import mapParse
from functions import components
from classes import core
from classes import enemy
from classes import projectile
from classes import tower
import savefiles
import classes
import data
import sounds
import random
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
# easy: -25% hp on enemies, long path (85), -25% score
# med: no speed modification, normal path (73), normal score
# hard: +25% hp on enemies, short path (56), +25% score


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
menuScreenButtonFont = pygame.font.SysFont('Arial', 30,  False)
menuScreenHeaderFont = pygame.font.SysFont('Arial', 45,  True)
menuScreenHeaderFont.set_underline(True)  # sets underline for a font

# initialize maps
mapList = ["easy", "med", "hard"]  # map file names
mapNames = ["Breezy Meadows", "Meandering Forest", "Blazing Desert"]  # map display names
selectedMap = "none"
numToDifficulty = ["easy", "med", "hard"]

# menu screen colours
colBackground = [200, 225, 255]

# list to hold rect objects and their colour
buttons = []
buttonsCol = []

# create list of level select buttons and their colour
mapInfo = []
for i in range(len(mapList)):
    mapInfo.append(mapParse.parse_coords(mapList[i]))
    buttonsCol.append([mapInfo[i][1], mapInfo[i][2]])
    buttons.append(pygame.Rect(450, 350 + i * 120, 400, 100))

# load hardcoded images
titlePic = load_pics("images/UI/", "title")
circlePic = load_pics("images/UI/", "dots")
otherShapesPic = load_pics("images/UI/", "shapes")
circleX = [0, 425, 850, 1275]
shapesX = [-425, 0, 425, 850]

# ---- LOAD CLASSES ----
# towers (turrets + boosters)
turretNames = ['basic turret','machinegun', 'sniper', 'cannon', 'frost', 'laser']
boosterNames = []
# list of towers and boosters available for purchase, taken from towerNames and boosterNames
turretList = []
boosterList = []
# UI button initialization
buttonListTowers = []
buttonListBoosters = []

# create tower buttons and add the tower classes
for i in range(len(turretNames)):
    turretList.append(tower.Turret(turretNames[i]))
    if i % 2 == 0:
        buttonListTowers.append(pygame.Rect(100, 75 + (i // 2) * 75, 50, 50))
    else:
        buttonListTowers.append(pygame.Rect(100, 175 + (i // 2) * 75, 50, 50))

# create booster buttons and add the booster classes
for i in range(len(boosterList)):
    if i % 2 == 0:
        buttonListTowers.append(pygame.Rect(300, 75 + (i // 2) * 75, 50, 50))
    else:
        buttonListTowers.append(pygame.Rect(300, 175 + (i // 2) * 75, 50, 50))

# load pictures of towers
turretPics = [load_pics("images/towers/", turretList[x].spriteBase) for x in range(len(turretList))]
boosterPics = [load_pics("images/towers/", boosterList[x].spriteBase) for x in range(len(boosterList))]

# ---- OUTER LOOP ----
while True:
    # ---- INTRO SCREEN ----
    while intro:
        # should make it 60FPS max
        # dt is the number of seconds since the last frame, use this for calculations instead of fps to make it smoother
        dt = clock.tick(60) / 1000
        if dt > 0.05:
            dt = 0.05
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            pygame.event.pump()

        # background
        screen.fill(colBackground)

        # draw the buttons and their text
        for i in range(len(buttons)):
            pygame.draw.rect(screen, buttonsCol[i][0], buttons[i])
            pygame.draw.rect(screen, (0, 0, 0), buttons[i], 1)
            # create a the button text based on the name and difficulty of the map
            components.create_text(screen, (buttons[i][0] + buttons[i][2] // 2, buttons[i][1] + buttons[i][3] // 2),
                                   mapNames[i] + " (" + numToDifficulty[int(mapInfo[i][0]) - 1] + ")",
                                   True, menuScreenButtonFont, (15, 15, 15))

        # draw prompt msg
        components.create_text(screen, (disLength // 2, 300),
                               "Choose a level", True, menuScreenHeaderFont, (0, 0, 0))

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

        # title text
        screen.blit(titlePic, (250, 50))
        # move circles using list comprehension
        circleX = [x - 100 * dt for x in circleX]
        for i in range(len(circleX)):
            if circleX[i] < - 425:
                circleX[i] += 1700
            # draw dot under title!
            screen.blit(circlePic, (int(circleX[i]), 175))
        # move other shapes using list comprehension
        shapesX = [x + 50 * dt for x in shapesX]
        for i in range(len(shapesX)):
            if shapesX[i] > 1325:
                shapesX[i] -= 1700
            # draw shapes!
            screen.blit(otherShapesPic, (int(shapesX[i]), 225))

        # border
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disLength, disHeight), 3)

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()

    # ---- IN-GAME SETUP ----

    # get path for the selected map only, instead of all of them
    mapInfo = mapParse.parse_coords(selectedMap)

    # convert grid info to pixel coords
    pathCoords = []
    for i in range(4, len(mapInfo), 1):
        pathCoords.append([mapInfo[i][0] * 50 - 25, mapInfo[i][1] * 50 - 25])

    # change score multiplier based on first pathCorners value (the map difficulty)
    # easy = 0.75x, med = 1x, hard = 1.25x
    scoreMulti = (mapInfo[0] + 2) / 4

    # get the random scattered sprite
    scatterSprite = load_pics("images/map/", mapInfo[3])
    scatterXY = []
    for i in range(random.randint(8, 12)):
        # generate random x y coords for them, x2 number of tiles.
        newThingy = [random.randint(1, 40), random.randint(1, 30), random.randint(0, 359)]
        if newThingy not in scatterXY:
            scatterXY.append(newThingy)

    # Colours of various objects
    colGrass = mapInfo[1]
    colPath = mapInfo[2]
    colGrid = [colGrass[0] - 20, colGrass[1] - 20, colGrass[2] - 20]
    colPurchaseMenu = [225, 225, 225]

    # delete unnecessary path corners info
    del(mapInfo[0])
    del(mapInfo[1])
    del(mapInfo[2])
    del(mapInfo[3])

    # ---- GAME LOOP ----
    while not intro:
        # should make it 60FPS max
        # dt is the number of seconds since the last frame, use this for calculations instead of fps to make it smoother
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # ---- BACKGROUND ----
        screen.fill(colGrass)
        # path and grid
        components.draw_grid(screen, 0, 0, disLength - 300, disHeight, 50, colGrid, False)
        components.draw_path(screen, pathCoords, colPath)

        # background scatter
        for i in range(len(scatterXY)):
            screen.blit(pygame.transform.rotate(scatterSprite, scatterXY[i][2]),
                        (scatterXY[i][0] * 25, scatterXY[i][1] * 25))

        # ---- UI ELEMENTS ----
        # ui background
        pygame.draw.rect(screen, colPurchaseMenu, (disLength - 300, 0, 300, disHeight), 0)

        # borders
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disLength, disHeight), 3)
        pygame.draw.line(screen, (0, 0, 0), (disLength - 300, 0), (disLength - 300, disHeight), 3)

        # purchase towers
        for i in range(len(turretList)):
            pass

        # update display!
        pygame.display.update()



