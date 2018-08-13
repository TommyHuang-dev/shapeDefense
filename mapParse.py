from data import maps

# this function parses a map data file for the coordinates and difficulty
def parseCoords(file_name):
    # setup file and return list
    file = open("data/maps/" + file_name, "r")
    corners = []
    # read first line for difficulty
    cur_line = int(file.readline())
    corners.append(cur_line)
    # get all corners
    for line in file:
        cur_line = line.split()
        if len(cur_line) == 2:
            corners.append([int(cur_line[0]), int(cur_line[1])])
        elif len(cur_line) == 3:
            corners.append([int(cur_line[0]), int(cur_line[1]), int(cur_line[2])])

    return corners

