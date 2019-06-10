# this function parses a map data file for the coordinates and difficulty
def parse_wave_info(file_name):
    # setup file and return list
    file = open("data/" + file_name, "r")
    wave_info = []  # list of lists. Inside each array is the following: [enemy name, amount, delay, interval]
    cur_wave = 0

    for line in file:
        if len(line.strip()) != 0:
            if line.split()[0] == 'wave':  # new wave
                cur_wave = int(line.split()[1])
                while len(wave_info) < cur_wave:
                    wave_info.append([])  # add new sub list, array index + 1 = waves
            else:  # get enemy name, then moar stuff
                cur_line = line.split()
                enemy_name = ' '.join(map(str, cur_line))  # joins all words together into a string
                cur_line = file.readline().split()
                amount = int(cur_line[0])
                delay = float(cur_line[1])
                interval = float(cur_line[2])
                wave_info[cur_wave - 1].append([enemy_name, amount, delay, interval])

    return wave_info