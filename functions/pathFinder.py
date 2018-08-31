# a simple algorithm to find a path between 2 points, not very efficient (flood fill)
ret_path = -1
searched_map = []  # list of all tiles already searched


def find_a_path(start, end, obs):
    global ret_path, searched_map
    ret_path = -1
    searched_map = []  # list of all tiles already searched

    def search(cur_tile, goal, path, obstacles):
        global searched_map, ret_path
        path.append(cur_tile)
        # check for goal

        # checking and stuffs
        if cur_tile in obstacles or cur_tile in searched_map:
            pass
        elif cur_tile == goal:
            ret_path = path
        elif cur_tile[0] > 20 or cur_tile[0] < 1 and cur_tile != path[0]:
            pass
        elif cur_tile[1] > 15 or cur_tile[1] < 1 and cur_tile != path[0]:
            pass
        elif ret_path == -1:  # RECURSIONNN
            searched_map.append(cur_tile)
            # right
            search([cur_tile[0] + 1, cur_tile[1]], goal, path.copy(), obstacles)
            # down
            search([cur_tile[0], cur_tile[1] + 1], goal, path.copy(), obstacles)
            # left
            search([cur_tile[0] - 1, cur_tile[1]], goal, path.copy(), obstacles)
            # up
            search([cur_tile[0], cur_tile[1] - 1], goal, path.copy(), obstacles)

    search(start, end, [], obs)
    return ret_path