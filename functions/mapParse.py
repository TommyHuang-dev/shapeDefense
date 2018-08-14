from data import maps

# this function parses a map data file for the coordinates and difficulty
def parse_coords(file_name):
    # setup file and return list
    file = open("data/maps/" + file_name, "r")
    map_info = []
    # read first line for difficulty
    cur_line = int(file.readline())
    map_info.append(cur_line)
    for line in file:
        cur_line = line.split()
        # corners
        if cur_line[0] == "obstacles":
            break
        if len(cur_line) == 2:
            map_info.append([int(cur_line[0]), int(cur_line[1])])
        # colour scheme
        elif len(cur_line) == 3:
            map_info.append([int(cur_line[0]), int(cur_line[1]), int(cur_line[2])])

    return map_info


def parse_obstacles(file_name):
    # setup file and return list
    file = open("data/maps/" + file_name, "r")
    ob_info = []
    start_read = False
    # read first line for difficulty
    for line in file:
        cur_line = line.split()
        # corners
        if cur_line[0] == "obstacles":
            start_read = True
        if start_read:
            if len(cur_line) == 2:
                ob_info.append([int(cur_line[0]), int(cur_line[1])])
            # colour scheme
            elif len(cur_line) == 3:
                ob_info.append([int(cur_line[0]), int(cur_line[1]), int(cur_line[2])])

    return ob_info
