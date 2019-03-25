import pygame


def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


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
            elif line.split()[0] == 'sprite':
                sprite = (' '.join(map(str, line.split())))[7:]
                enemy_info[cur_enemy]['sprite'] = load_pics('images/enemies/', sprite)
            elif line.split()[0] == 'death_spawn_enemy':
                death_spawn = (' '.join(map(str, line.split())))[18:]
                enemy_info[cur_enemy]['death_spawn_enemy'] = death_spawn
            # append information as follows: enemy_info[name][attribute][value] (dictionary of dictionaries of lists)
            else:
                enemy_info[cur_enemy][line.split()[0]] = line.split()[1]

    return enemy_info
