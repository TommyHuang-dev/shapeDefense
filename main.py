from functions import components
from classes import enemy
from classes import projectile
from classes import tower
from classes import map
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
disL = 1300  # right 300 used for buying stuff and menu
disH = 750  # all 750 used for the map (1000 x 750 = 20 x 15 tiles)
screen = pygame.display.set_mode((disL, disH))
pygame.display.set_caption("Shape Defense")

intro = True

# font stuff
menuScreenButtonFont = pygame.font.SysFont('Arial', 30,  False)
menuScreenHeaderFont = pygame.font.SysFont('Arial', 45,  True)
menuScreenHeaderFont.set_underline(True)  # sets underline for a font

# initialize maps
mapList = ["1", "2", "3", "4", "5", "6"]  # map file names
mapButtonNames = ["1", "2", "3", "4", "5", "6"]  # map display names
mapDisplayNames = ["Open Trial", "Parallel Waves", "Curved Path", "Three Lines", "Intersection", "Chaotic Spiral"]
selectedMap = "none"  # map class

# colours of stuff
colBackground = [200, 225, 255]
colPurchaseMenu = [220, 220, 240]

# list to hold rect objects and their colour
buttons = []
buttonsCol = []

# create list of level select buttons and their colour
mapInfo = []
for i in range(len(mapList)):
    mapInfo.append(map.Map(mapList[i]))
    buttonsCol.append([mapInfo[i].colBackground, mapInfo[i].colObs])
    if i % 2 == 0:
        buttons.append(pygame.Rect(560, 350 + (i // 2) * 100, 80, 80))
    else:
        buttons.append(pygame.Rect(660, 350 + (i // 2) * 100, 80, 80))

# load hardcoded images
titlePic = load_pics("images/UI/", "title")
circlePic = load_pics("images/UI/", "dots")
otherShapesPic = load_pics("images/UI/", "shapes")
circleX = [0, 425, 850, 1275]
shapesX = [-425, 0, 425, 850]

# ---- LOAD CLASSES ----
# list of purchasable towers (turrets + boosters)
turretNames = ['basic turret', 'wall']
boosterNames = []
# list of towers and boosters available for purchase, taken from towerNames and boosterNames
turretList = []
boosterList = []
# UI button initialization
buttonListTurrets = []
buttonListBoosters = []

# create tower buttons and add the tower classes
for i in range(len(turretNames)):
    turretList.append(tower.Turret(turretNames[i]))
    # append rect objects to the list
    if i % 3 == 0:
        buttonListTurrets.append(pygame.Rect(disL - 250, 50 + (i // 3) * 75, 50, 50))
    elif i % 3 == 1:
        buttonListTurrets.append(pygame.Rect(disL - 175, 50 + (i // 3) * 75, 50, 50))
    elif i % 3 == 2:
        buttonListTurrets.append(pygame.Rect(disL - 100, 50 + (i // 3) * 75, 50, 50))

# create booster buttons and add the booster classes
for i in range(len(boosterNames)):
    boosterList.append(tower.Booster(boosterNames[i]))
    # append rect objects to the list
    if i % 3 == 0:
        buttonListTurrets.append(pygame.Rect(disL - 250, 300 + (i // 3) * 75, 50, 50))
    elif i % 3 == 1:
        buttonListTurrets.append(pygame.Rect(disL - 175, 300 + (i // 3) * 75, 50, 50))
    elif i % 3 == 2:
        buttonListTurrets.append(pygame.Rect(disL - 100, 300 + (i // 3) * 75, 50, 50))

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
        if dt > 0.05:  # maximum delta time
            dt = 0.05
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # background
        screen.fill(colBackground)

        # get mouse press on a button
        mousePos = pygame.mouse.get_pos()
        for i in range(len(buttons)):
            if buttons[i].collidepoint(mousePos):
                # on hover, draw thicker outline and a preview of the map
                pygame.draw.rect(screen, (0, 0, 0), buttons[i], 3)
                # map preview:
                mapInfo[i].draw_preview(screen, disL - 500, disH - 400, 0.4)
                pygame.draw.rect(screen, (0, 0, 0), (disL - 500, disH - 400, 400, 300), 1)

                # on click, set map and close out intro
                if pygame.mouse.get_pressed()[0] == 1:
                    selectedMap = mapInfo[i]
                    intro = False

        # draw the buttons and their text
        for i in range(len(buttons)):
            pygame.draw.rect(screen, buttonsCol[i][0], buttons[i])
            pygame.draw.rect(screen, (0, 0, 0), buttons[i], 1)
            # create a the button text based on the name and difficulty of the map
            components.create_text(screen,
                                   (buttons[i][0] + buttons[i][2] // 2, buttons[i][1] + buttons[i][3] // 2),
                                   mapButtonNames[i], True, menuScreenButtonFont, (15, 15, 15))

        # draw prompt msg
        components.create_text(screen, (disL // 2, 300),
                               "Choose a level", True, menuScreenHeaderFont, (0, 0, 0))

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
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disL, disH), 3)

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()

    # ---- IN-GAME SETUP and reset variables----
    money = 300
    power = [0, 10]  # amount of power used vs maximum
    income = 50

    # ---- GAME LOOP ----
    while not intro:
        # should make it 60FPS max
        # dt is the number of seconds since the last frame, use this for calculations instead of fps to make it smoother
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # ---- BACKGROUND ----
        screen.fill(selectedMap.colBackground)
        # path and obstacles
        components.draw_grid(screen, 0, 0, disL - 300, disH, 50, selectedMap.colGrid, False)
        selectedMap.draw_obstacles(screen)

        # ---- UI ELEMENTS ----
        # ui background
        pygame.draw.rect(screen, colPurchaseMenu, (disL - 300, 0, 300, disH), 0)

        # borders
        pygame.draw.rect(screen, selectedMap.colObs, (0, 0, disL, disH), 3)
        pygame.draw.line(screen, selectedMap.colObs, (disL - 300, 0), (disL - 300, disH), 3)

        # purchase tower buttons
        for i in range(len(turretList)):
            pygame.draw.rect(screen, (0, 0, 0), (buttonListTurrets[i]), 1)
            screen.blit(turretPics[i], (buttonListTurrets[i][0], buttonListTurrets[i][1]))

        # update display!
        pygame.display.update()
