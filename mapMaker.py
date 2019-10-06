import pygame
import sys
import functions.components

# lightweight program that makes making maps easier
# left click to add obstacles (walls) to the map
# middle click to add an entrance, then click again for an exit. Please only add these on map edges.
# right click to remove obstacles or entrances.
# converts xy pixel value to a grid coord for map-maker
def xy_to_pos(xy, grid_size):
    pos = [xy[0] // grid_size, xy[1] // grid_size]
    # make sure its not out of bounds
    if pos[0] > 21:
        pos[0] = 21
    elif pos[0] < 0:
        pos[0] = 0
    if pos[1] > 16:
        pos[1] = 16
    elif pos[1] < 0:
        pos[1] = 0

    return pos


pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()
fps = 60
disL = 550
disH = 425 
screen = pygame.display.set_mode((disL, disH))
pygame.display.set_caption("Shape Defense Map Maker")

f_out = "data/maps/temp"
f_in = "data/maps/temp"
# coordinates of all spawners and exits
spawnLocList = []  # list of lists e.g. [[2, 3, 4, 7]]

# coordinates of all obstacles. e.g. [1, 2]
obsLocList = []

# some global params
spawnerPlaced = None  # if not none, then a spawner was placed. Place exit next time!

textFont = pygame.font.SysFont('Trebuchet MS', 11, False)

# initialize to current temp
readingSpawners = False
readingObstacles = False
with open(f_in, "r") as f:
    for line in f:
        if len(line.strip()) != 0:
            line = line.split()
        
            if line[0] == "spawns":
                readingSpawners = True
                readingObstacles = False
            elif line[0] == "obstacles":
                readingSpawners = False
                readingObstacles = True

            elif readingSpawners:
                spawnLocList.append([int(line[0]), int(line[1]), int(line[2]), int(line[3])])
            elif readingObstacles:
                obsLocList.append([int(line[0]), int(line[1])])


while True:
    for event in pygame.event.get():
        # if game exits, output to file
        if event.type == pygame.QUIT:
            with open(f_out, "w+") as f:
                f.write("MAP NAME HERE\n")
                f.write("220 230 220\n")
                f.write("40 40 40\n")
                f.write("spawns\n")
                for i in spawnLocList:
                    for j in range(4):
                        f.write(str(i[j]) + " ")
                    f.write("\n")

                f.write("obstacles\n")
                for i in obsLocList:
                    for j in range(2):
                        f.write(str(i[j]) + " ")
                    f.write(" 1 1\n")

            sys.exit()

    #  screen.fill(colBackground) start of da program -----------
    pygame.display.update()
    clock.tick(fps)
    mousePos = pygame.mouse.get_pos()
    mousePressed =  pygame.mouse.get_pressed()

    # clickity click 
    screen.fill([200, 220, 235])
    
    # wow I actually made this function useful
    functions.components.draw_grid(screen, 0, 0, disL, disH, 25, (150, 150, 150), False)
    pygame.draw.rect(screen, (150, 50, 60), (25, 25, 500, 375), 3)
    curPos = xy_to_pos((mousePos[0], mousePos[1]), 25)
    
    # draw obstacles
    for i in obsLocList:
        pygame.draw.rect(screen, (30, 30, 30), (i[0] * 25, i[1] * 25, 25, 25))
    # draw spawners
    for i in spawnLocList:
        pygame.draw.rect(screen, (50, 220, 50), (i[0] * 25, i[1] * 25, 25, 25))
        pygame.draw.rect(screen, (220, 50, 50), (i[2] * 25, i[3] * 25, 25, 25))
        functions.components.create_text((screen), (i[0] * 25 + 12, i[1] * 25 + 12), str(spawnLocList.index(i)), True, textFont, (0, 0, 0))
        functions.components.create_text((screen), (i[2] * 25 + 12, i[3] * 25 + 12), str(spawnLocList.index(i)), True, textFont, (0, 0, 0))
    # draw potential new spawner
    if spawnerPlaced != None:
        pygame.draw.rect(screen, (50, 150, 50), (spawnerPlaced[0] * 25, spawnerPlaced[1] * 25, 25, 25))

    # remove elements
    if mousePressed[2] == 1:
        # remove spawners
        for i in range(len(spawnLocList)):
            if curPos == [spawnLocList[i][0], spawnLocList[i][1]] or curPos == [spawnLocList[i][2], spawnLocList[i][3]]:
                del(spawnLocList[i])
                break

        for i in range(len(obsLocList)):
            if curPos in obsLocList:
                del(obsLocList[obsLocList.index(curPos)])

    # create obstacle
    if mousePressed[0] == 1:
        if curPos not in obsLocList:
            obsLocList.append(curPos)

    # create spawn
    if mousePressed[1] == 1:
        if spawnerPlaced == None:
            # update spawnerplaced:
            spawnerPlaced = curPos

        for i in range(len(spawnLocList)):
            if curPos == [spawnLocList[i][0], spawnLocList[i][1]] or curPos == [spawnLocList[i][2], spawnLocList[i][3]]:
                spawnerPlaced = None
                break

        if spawnerPlaced != None and curPos != spawnerPlaced:
            spawnLocList.append([spawnerPlaced[0], spawnerPlaced[1], curPos[0], curPos[1]])
            spawnerPlaced = None

