# a simple breadth-first algorithm to find a path between 2 points, not very efficient (flood fill)


# algorithm: fill the map with how many moves is needed to get to a certin tile
# afterwards, backtrack from the ending point, going down exactly one each time, guaranteed to find shortest route
def find_a_path(start, end, obs):
    ret_path = -1  # -1 if no path found, or a list of coords if it finds one
    searched_map = []
    for i in range(22):
        # initialize list of all tiles already searched, and how many moves to get to there
        searched_map.append([-1 for j in range(17)])

    # initialize tiles
    next_tiles = [start]
    cur_moves = -1

    # find distance to all tiles by flood filling
    while len(next_tiles) > 0:
        # step and fill
        cur_tiles = [[next_tiles[i][0], next_tiles[i][1]] for i in range(len(next_tiles))]
        next_tiles.clear()
        cur_moves += 1
        # do da searching
        for i in range(len(cur_tiles)):
            # make sure its within boundaries
            if (1 <= cur_tiles[i][0] <= 20 and 1 <= cur_tiles[i][1] <= 15) \
                    or cur_tiles[i] == start or cur_tiles[i] == end:
                # make sure its not touching a tower or wall, or was already checked
                if cur_tiles[i] not in obs and searched_map[cur_tiles[i][0]][cur_tiles[i][1]] == -1:
                    # add to searched_map
                    searched_map[cur_tiles[i][0]][cur_tiles[i][1]] = cur_moves
                    # add more tiles to search next time
                    next_tiles.append([cur_tiles[i][0] + 1, cur_tiles[i][1]])  # right
                    next_tiles.append([cur_tiles[i][0], cur_tiles[i][1] + 1])  # down
                    next_tiles.append([cur_tiles[i][0] - 1, cur_tiles[i][1]])  # left
                    next_tiles.append([cur_tiles[i][0], cur_tiles[i][1] - 1])  # up

    ret_path = [end]
    bt_moves = searched_map[end[0]][end[1]]
    
    while ret_path[0] != start:
        bt_moves -= 1

        # insert items to the beginning if a lower number is found
        # up
        if ret_path[0][1] - 1 >= 0 and searched_map[ret_path[0][0]][ret_path[0][1] - 1] == bt_moves:
            ret_path.insert(0, [ret_path[0][0], ret_path[0][1] - 1])
        # down
        elif ret_path[0][1] + 1 <= 16 and searched_map[ret_path[0][0]][ret_path[0][1] + 1] == bt_moves:
            ret_path.insert(0, [ret_path[0][0], ret_path[0][1] + 1])
        # left
        elif ret_path[0][0] - 1 >= 0 and searched_map[ret_path[0][0] - 1][ret_path[0][1]] == bt_moves:
            ret_path.insert(0, [ret_path[0][0] - 1, ret_path[0][1]])
        # right
        elif ret_path[0][0] + 1 <= 21 and searched_map[ret_path[0][0] + 1][ret_path[0][1]] == bt_moves:
            ret_path.insert(0, [ret_path[0][0] + 1, ret_path[0][1]])
        else:
            return -1

    return ret_path
