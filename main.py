from functions import components
from functions import creditParse
from functions import waveParse
from classes import enemy
from classes import projectile
from classes import tower
from classes import map
import savefiles
import classes
import data
import sounds
import random
import os.path
import time
import pygame
from pygame import gfxdraw
import sys


def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


def display_stats(sel_tower):
    # not placed tower, display cost
    if not sel_tower.placed:
        # not enough money
        if sel_tower.cost > money:
            # display cost as red text
            components.create_text(screen, (disL - 275, 420), "$" + str(sel_tower.cost),
                                   False, levelTowerFont, (200, 25, 25))
        # enough monies
        else:
            # display cost
            components.create_text(screen, (disL - 275, 420), "$" + str(sel_tower.cost),
                                   False, levelTowerFont, (0, 0, 0))
    # placed tower, display level
    elif sel_tower.placed:
        tempString = "level "
        if sel_tower.curLevel > 1 and sel_tower.curLevel == sel_tower.maxLevel:  # max level
            tempString += "MAX"
        elif sel_tower.maxLevel == 1:  # not upgradable (i.e. walls)
            tempString = ""
        else:  # display level
            tempString += str(sel_tower.curLevel)
        # display cost as red text
        components.create_text(screen, (disL - 275, 420), tempString,
                               False, levelTowerFont, (0, 0, 0))

    # show some stats (name, damage, fire rate, etc.)
    components.create_text(screen, (disL - 150, 380), sel_tower.name, True,
                           levelTowerTitleFont, (0, 50, 175))


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
pygame.mixer.pre_init(22050, -16, 8, 512)
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

# font stuff: ms = menu screen
msLevelSelectFont = pygame.font.SysFont('Trebuchet MS', 32, False)
msMenuButFont = pygame.font.SysFont('Trebuchet MS', 45, True)
msHeaderFont = pygame.font.SysFont('Trebuchet MS', 40, True)
msHeaderFont.set_underline(True)

levelInfoFont = pygame.font.SysFont('Trebuchet MS', 28, False)
levelTowerTitleFont = pygame.font.SysFont('Trebuchet MS', 28, True)
levelTowerTitleFont.set_underline(True)
levelTowerFont = pygame.font.SysFont('Trebuchet MS', 22, False)
levelNextWaveFont = pygame.font.SysFont('Trebuchet MS', 40, True)

creditHeaderFont = pygame.font.SysFont('Trebuchet MS', 30, True)
creditBodyFont = pygame.font.SysFont('Trebuchet MS', 24, False)

# initialize maps
mapList = ["1", "2", "3", "4", "5", "6"]  # map file names
selectedMap = "none"  # map class

# initialize sounds
soundClick = pygame.mixer.Sound("sounds/UI/button.wav")
soundError = pygame.mixer.Sound("sounds/UI/error.wav")
soundSell = pygame.mixer.Sound("sounds/UI/sell.wav")
soundPlaced = pygame.mixer.Sound("sounds/game/placed_down.wav")
soundLevelSelect = pygame.mixer.Sound("sounds/UI/level_select.wav")

musicMenu = pygame.mixer.music.load('sounds/menu.ogg')
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)

# colours of stuff
colBackground = [200, 225, 255]
colPurchaseMenu = [220, 220, 240]

# list to hold rect objects and their colour
levelBut = []
levelButCol = []

# create list of level select levelBut and their colour
mapInfo = []
for i in range(len(mapList)):
    mapInfo.append(map.Map(mapList[i]))
    levelButCol.append([mapInfo[i].colBackground, mapInfo[i].colObs])
    if i % 2 == 0:
        levelBut.append(pygame.Rect(470, 360 + (i // 2) * 100, 80, 80))
    else:
        levelBut.append(pygame.Rect(570, 360 + (i // 2) * 100, 80, 80))

# create list of menu levelBut (e.g. play, settings, etc.)
menuButText = ["PLAY", "credits"]
menuButCol = [[100, 240, 100], [240, 230, 120]]
menuBut = [pygame.Rect(90, 310 + i * 115, 250, 100) for i in range(len(menuButText))]
butPressed = 'none'

# load hardcoded images
titlePic = load_pics("images/UI/", "title")
circlePic = load_pics("images/UI/", "dots")
otherShapesPic = load_pics("images/UI/", "shapes")
circleX = [0, 425, 850, 1275]
shapesX = [-425, 0, 425, 850]

moneyPic = load_pics("images/UI/", "symbol_money")
lifePic = load_pics("images/UI/", "symbol_life")
energyPic = load_pics("images/UI/", "symbol_electricity")

# credits
creditText = creditParse.parse("data/credits")

# ---- LOAD CLASSES ----
# list of purchasable towers (turrets, boosters)
towerNames = ['Wall', 'Basic Turret', 'Sniper Turret']
# list of towers and boosters available for purchase, taken from towerNames and boosterNames
towerList = []
# UI button initialization
butListTowers = []

# create tower levelBut and add the tower classes
for i in range(len(towerNames)):
    towerList.append(tower.Turret(towerNames[i]))

# create turret buttons
for i in range(6):
    if i % 3 == 0:
        butListTowers.append(pygame.Rect(disL - 270, 170 + (i // 3) * 80, 70, 70))
    elif i % 3 == 1:
        butListTowers.append(pygame.Rect(disL - 185, 170 + (i // 3) * 80, 70, 70))
    elif i % 3 == 2:
        butListTowers.append(pygame.Rect(disL - 100, 170 + (i // 3) * 80, 70, 70))

# projectile image loading (uses a dictionary)
projImgList = {}
for i in range(len(towerList)):
    # get name of projectile
    nextImgName = towerList[i].stats['sprite_proj'][0] + "-hit"
    curImg = 0
    while True:
        projImgList[nextImgName] = load_pics("images/hit_effects/", nextImgName + str(curImg))
        if os.path.isfile("images/hit_effects/" + nextImgName + str(curImg + 1)):
            curImg += 1
        else:
            break

# switch page button image for puchase menu
imgNextPage = load_pics("images/UI/", "nextPg")
imgPrevPage = load_pics("images/UI/", "prevPg")
butNextPage = pygame.Rect(disL - 130 + 2, butListTowers[0][1] + 150 + 2,
                          imgNextPage.get_width() - 4, imgNextPage.get_height() - 4)
butPrevPage = pygame.Rect(disL - 200 + 2, butListTowers[0][1] + 150 - 2,
                          imgPrevPage.get_width() - 4, imgPrevPage.get_height() - 4)

# menu NEXT WAVE button
butNextWave = pygame.Rect(disL - 275, disH - 90, 250, 80)
butNextWaveCol = [[175, 175, 175], [100, 225, 120]]  # colour for round in progress vs. not in progress

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

        # menu levelButCol
        for i in range(len(menuButText)):
            pygame.draw.rect(screen, menuButCol[i], menuBut[i])
            components.create_text(screen, (int(menuBut[i][0] + menuBut[i][2] / 2),
                                            int(menuBut[i][1] + menuBut[i][3] / 2)),
                                   menuButText[i], True, msMenuButFont, (0, 0, 0))

        # get mouse press on a button
        mousePos = pygame.mouse.get_pos()

        # draw menu levelBut
        for i in range(len(menuBut)):
            if menuBut[i].collidepoint(mousePos[0], mousePos[1]):
                # draw thicker outline on hover
                pygame.draw.rect(screen, (0, 0, 0), menuBut[i], 3)
                if pygame.mouse.get_pressed()[0] == 1 and butPressed != menuButText[i]:
                    soundClick.play()
                    butPressed = menuButText[i]
            # draw a thick red outline if it was selected
            if butPressed == menuButText[i]:
                pygame.draw.rect(screen, (150, 25, 25), menuBut[i], 3)
            # otherwise don't draw anything
            else:
                pygame.draw.rect(screen, (0, 0, 0), menuBut[i], 1)

        # draw level select levelBut after play is clicked
        if butPressed == "PLAY":
            for i in range(len(levelBut)):
                if levelBut[i].collidepoint(mousePos[0], mousePos[1]):
                    # on hover, draw thicker outline and a preview of the map
                    pygame.draw.rect(screen, (0, 0, 0), levelBut[i], 3)
                    # map preview:
                    mapInfo[i].draw_preview(screen, disL - 500, 360, 0.4)
                    pygame.draw.rect(screen, (0, 0, 0), (disL - 500, 360, 400, 300), 1)
                    components.create_text(screen, [disL - 300, 340], mapInfo[i].mapName, True,
                                           msLevelSelectFont, (0, 0, 0))

                    # on click, set map and close out intro
                    if pygame.mouse.get_pressed()[0] == 1:
                        soundLevelSelect.play()
                        selectedMap = mapInfo[i]
                        intro = False

            # draw the levelBut and their text
            for i in range(len(levelBut)):
                pygame.draw.rect(screen, levelButCol[i][0], levelBut[i])
                pygame.draw.rect(screen, (0, 0, 0), levelBut[i], 1)
                # create a the button text based on the name and difficulty of the map
                components.create_text(screen,
                                       (levelBut[i][0] + levelBut[i][2] // 2, levelBut[i][1] + levelBut[i][3] // 2),
                                       i + 1, True, msLevelSelectFont, (15, 15, 15))

            # draw prompt msg
            components.create_text(screen, (int(levelBut[0][0] + levelBut[1][0] + levelBut[0][2] * 1 + 10) / 2, 315),
                                   "Choose a level", True, msHeaderFont, (0, 0, 0))

        elif butPressed == "credits":
            # credit title
            components.create_text(screen, (400, 340), creditText[0], False, creditHeaderFont, (0, 0, 0))
            # create rest of credits
            for i in range(1, len(creditText)):
                components.create_text(screen, (400, 340 + i * 40), creditText[i], False, creditBodyFont, (0, 0, 0))

        # title text
        screen.blit(titlePic, (250, 50))
        # move circles using list comprehension
        circleX = [x - 140 * dt for x in circleX]
        for i in range(len(circleX)):
            if circleX[i] < - 425:
                circleX[i] += 1700
            # draw dot under title!
            screen.blit(circlePic, (int(circleX[i]), 175))
        # move other shapes using list comprehension
        shapesX = [x + 70 * dt for x in shapesX]
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

    # stop intro song
    pygame.mixer.music.stop()

    # ---- IN-GAME SETUP and reset variables----
    curWave = 0  # current wave
    money = 500  # starting monies
    energy = [0, 10]  # amount of power used vs maximum
    income = 100  # monies per round
    life = 30  # lose 1 life per enemy; 10 per boss
    currentlyInWave = False  # True when enemies are spawning

    # page that its on
    curPurchasePage = 0

    # mouse stuff
    mousePressed = pygame.mouse.get_pressed()
    selectedTower = 'none'
    selectedXY = [0, 0]
    selectedPos = [0, 0]

    # viewing placed towers
    viewedTower = -1  # index position of a placed tower, -1 if no tower

    # placed towers
    placedTowers = []  # list of tower objects, placed down
    placedTowersLoc = []  # used so that you cant overlap two towers

    # music change
    musicGame = pygame.mixer.music.load('sounds/ingame.ogg')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    # parse wave info
    waveParse.parse_wave_info("waveData")

    # intro variables
    colIntro = [150, 165, 200, 255]
    introScreen = 60

    # OBSTACLE PATHING TEST
    path = selectedMap.find_path(placedTowers)

    # ---- GAME LOOP ----
    while not intro:
        # should make it 60FPS max
        # dt is the number of seconds since the last frame, use this for calculations instead of fps to make it smoother
        dt = clock.tick(60) / 1000
        mousePressed = [0, 0, 0]  # reset mouse presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = pygame.mouse.get_pressed()

        # get inputs
        mousePos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        hovered = False  # whether or not the mouse is hovering over a tower purchase button

        # make sure money doesn't go over maximum of 10000, and energy for 50
        if money > 10000:
            money = 10000
        if energy[0] > 50:
            energy[0] = 50

        # ---- BACKGROUND ----
        screen.fill(selectedMap.colBackground)
        # obstacles
        components.draw_grid(screen, 0, 0, disL - 300, disH, 50, selectedMap.colGrid, False)
        selectedMap.draw_obstacles(screen)

        # path
        for i in range(len(path[0])):
            pygame.draw.circle(screen, (0, 0, 0), (path[0][i][0] * 50 - 25, path[0][i][1] * 50 - 25), 5)

        # ---- TOWERS ----
        # draw placed towers:
        # tower base
        for i in range(len(placedTowers)):
            placedTowers[i].draw_tower_base(screen, [placedTowers[i].pos[0] * 50 - 25,
                                                     placedTowers[i].pos[1] * 50 - 25])
        # if a tower is viewed, draw the white outline here (before gun, after base)
        if viewedTower >= 0:
            display_stats(placedTowers[viewedTower])
            pygame.draw.rect(screen, (200, 75, 75), (placedTowers[viewedTower].pos[0] * 50 - 50,
                                                     placedTowers[viewedTower].pos[1] * 50 - 50, 50, 50), 3)
        # tower gun
        for i in range(len(placedTowers)):
            placedTowers[i].draw_tower_gun(screen, [placedTowers[i].pos[0] * 50 - 25,
                                                    placedTowers[i].pos[1] * 50 - 25], 0)

        # unselect a tower
        if (mousePos[0] > disL - 300 and mousePressed[0] == 1 or keys[pygame.K_ESCAPE]) and selectedTower != 'none':
            mousePressed = [0, 0]  # so you don't select another tower when unselecting
            selectedTower = 'none'

        # choose where to place down the tower, click to place
        if selectedTower != 'none':
            # calculate the validity of the current placement
            valid = False
            if 10 <= mousePos[0] <= disL - 310 and 10 <= mousePos[1] <= disH - 10 and selectedMap.calc_valid(mousePos)\
                    and components.xy_to_pos(mousePos) not in placedTowersLoc:
                valid = True

            # lock to grid inside it and draw range when valid
            if valid:
                gridLoc = components.xy_to_pos(mousePos)
                selectedTower.pos = [gridLoc[0], gridLoc[1]]
                selectedTower.draw_tower_full(screen, (selectedTower.pos[0] * 50 - 25, selectedTower.pos[1] * 50 - 25), 0)
                selectedTower.draw_range(screen, valid)

                # place down the tower when selected
                if mousePressed[0] == 1 and money >= selectedTower.cost:
                    soundPlaced.play()
                    # copy as a NEW object
                    placedTowers.append(tower.Turret(selectedTower.name))
                    placedTowers[-1].pos = selectedTower.pos
                    placedTowers[-1].placed = True  # set it to be placed!!
                    placedTowersLoc.append(selectedTower.pos)
                    # lower monies
                    money -= selectedTower.cost
                elif mousePressed[0] == 1:
                    soundError.play()

            # don't lock to grid if out of bounds
            elif not valid:
                selectedTower.draw_tower_full(screen, [mousePos[0], mousePos[1]], 0)
                selectedTower.draw_range(screen, valid, xy=[mousePos[0], mousePos[1]])
                if mousePressed[0] == 1:  # error if user tries to place invalid tower
                    soundError.play()

        # ---- UI ELEMENTS ----
        # ui background
        pygame.draw.rect(screen, colPurchaseMenu, (disL - 300, 0, 300, disH), 0)

        # borders
        pygame.draw.rect(screen, selectedMap.colObs, (0, 0, disL, disH), 3)
        pygame.draw.line(screen, selectedMap.colObs, (disL - 300, 0), (disL - 300, disH), 3)

        # sub dividers, from top to bottom
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, butListTowers[0][1] - 20), (disL, butListTowers[0][1] - 20))
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, butListTowers[0][1] + 180),
                         (disL, butListTowers[0][1] + 180))
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, disH - 80),
                         (disL, disH - 80))

        # switch page buttons
        if curPurchasePage > 0:  # previous page
            screen.blit(imgPrevPage, (disL - 200, butListTowers[0][1] + 150))
            # get hit box and mouse click
            if butPrevPage.collidepoint(mousePos[0], mousePos[1]) and mousePressed[0] == 1:
                soundClick.play()
                curPurchasePage -= 1
        if curPurchasePage < (len(towerList) - 1) // 6:  # next page
            screen.blit(imgNextPage, (disL - 130, butListTowers[0][1] + 150))
            # get hit box and mouse click
            if butNextPage.collidepoint(mousePos[0], mousePos[1]) and mousePressed[0] == 1:
                soundClick.play()
                curPurchasePage += 1

        # purchase tower images
        mul6 = curPurchasePage * 6
        # purchase tower actual buttons and outline
        for i in range(6):
            # select a tower
            if i + mul6 < len(towerList):
                pygame.draw.rect(screen, (230, 230, 250), (butListTowers[i]))
                # on hover
                if butListTowers[i].collidepoint(mousePos[0], mousePos[1]) and selectedTower == 'none':
                    hovered = True
                    display_stats(towerList[i + mul6])
                    # user has enough money to buy the tower
                    if towerList[i + mul6].cost <= money:
                        pygame.draw.rect(screen, (255, 255, 255), (butListTowers[i]), 2)
                        # purchase tower on click
                        if mousePressed[0] == 1:
                            soundClick.play()
                            selectedTower = towerList[i + mul6]
                    else:  # not enough money, play meep merp on purchase attempt
                        if mousePressed[0] == 1:
                            soundError.play()
                            selectedTower = 'none'

        for i in range(mul6, mul6 + 6, 1):
            # draw towers on top of the buttons
            if i < len(towerList):
                # draw base + gun for turret
                towerList[i].draw_tower_full(screen, [butListTowers[i - mul6][0] + butListTowers[i - mul6][2] // 2,
                                                      butListTowers[i - mul6][1] + butListTowers[i - mul6][3] // 2], 0)

        # show stats of selected tower
        if selectedTower != 'none':  # while placing
            # display stats of selected tower
            display_stats(selectedTower)
            viewedTower = -1
        else:  # tower on ground
            if mousePressed[0] == 1:
                if components.xy_to_pos(mousePos) in placedTowersLoc:
                    soundClick.play()
                    viewedTower = placedTowersLoc.index(components.xy_to_pos(mousePos))
                else:
                    viewedTower = -1

            # draw range of da tower
            if viewedTower >= 0:
                placedTowers[viewedTower].draw_range(screen, True)
                if not hovered:
                    display_stats(placedTowers[viewedTower])

        # info about money, life, etc.
        # life
        screen.blit(lifePic, (disL - 275, 20))
        components.create_text(screen, (disL - 210, 50), str(life), False, levelInfoFont, (0, 0, 0))
        # wave
        components.create_text(screen, (disL - 145, 50), "wave  " + str(curWave), False, levelInfoFont, (0, 0, 0))
        # money
        screen.blit(moneyPic, (disL - 275, 80))
        components.create_text(screen, (disL - 210, 110), str(int(money)), False, levelInfoFont, (0, 0, 0))
        # energy
        screen.blit(energyPic, (disL - 150, 80))
        components.create_text(screen, (disL - 100, 110), str(energy[0]) + "/" + str(energy[1]),
                               False, levelInfoFont, (0, 0, 0))

        # show a fading bluish screen after selecting the level
        if introScreen > 0:
            pygame.gfxdraw.filled_polygon(screen, [[0, 0], [disL, 0], [disL, disH], [0, disH]], colIntro)
            introScreen -= 1
            colIntro[3] = 10 + introScreen * 4

        # update display!
        pygame.display.update()
