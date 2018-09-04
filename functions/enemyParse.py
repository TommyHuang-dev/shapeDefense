
# reads a file and gets data for enemy stats
def get_data(file_name):
    enemy_info = {}
    file = open("data/" + file_name, "r")

    cur_enemy = ""
    for line in file:
        if len(line.strip()) != 0:
            # go for next enemy
            if line.split()[0] == 'name':
                cur_enemy = (' '.join(map(str, line.split())))[5:]
                enemy_info[cur_enemy] = {}
            # append information as follows: enemy_info[name][attribute][value] (dictionary of dictionaries of lists)
            else:
                enemy_info[cur_enemy][line.split()[0]] = line.split()[1]

    return enemy_info
