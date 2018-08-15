def get_stats(name):
    # initialize conditions
    data_file = open("data/towerData", "r")
    stat_list = {}
    start_read = False

    # run through all the lines until the desired name is found
    for line in data_file:
        # copy all the values in!
        if len(line.strip()) != 0:
            if start_read:
                cur_line = line.split()
                # stop reading when reaching a blank line
                if cur_line[0] == "end":
                    print(stat_list)
                    return stat_list
                print(cur_line)
                stat_key = cur_line[0]
                stat_val = cur_line[1:]
                stat_list[str(stat_key)] = stat_val
            # search for the tower
            else:
                if line.split()[0] == "name":
                    cur_line = ' '.join(map(str, line.split()[1:]))
                    if cur_line == name:
                        start_read = True
