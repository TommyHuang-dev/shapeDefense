import random

valueList = {}  # list of [['enemy name', cost], [...]].
# enemyValues file contains the base "cost" to spawn enemies. Higher cost = stronger enemy = less.
# additionally spawning enemies with less delay in between also costs more (default = 1sec)
with open("data/enemyValues", "r") as f:
    for line in f:
        if len(line.strip()) != 0:
            newLine = line.strip().split()
            cost = float(newLine[-1])
            del(newLine[-1])
            name = ' '.join(map(str, newLine))
            valueList[name] = cost

# outputs a new random wave with format: [['name', num, delay, interval], ['speedy', 12, 2.0, 0.75]]
def generate(wave):
    # total amount of power the wave will have. For reference:
    # wave 1 has 20 powerTotal and 1 powerRate
    # wave 35 has 336 powerTotal and 23 powerRate
    # wave 38 has 975 powerTotal and 26 powerRate
    # wave 40 has 960 powerTotal and 32 powerRate
    powerRandom = random.uniform(-4,4)  # make total power and rate inversely related
    powerTotal = (wave * 18) ** 1.04 + powerRandom * 50
    powerRate = 1 + wave * 0.65 - powerRandom * 1.0
    # number of different enemy types to spawn
    numEnemies = random.randint(2, 4)

    # 'boss' waves have a larger variety of enemies and more of them
    if wave % 5 == 0:
        print('boss wave!')
        numEnemies += 1
        powerTotal *= 1.25
    
    # Formation is how they will spawn (e.g. in groups, or just regularly):
    # 0,1: Regular: all enemies start spawning at beginning and spawn at uniform intervals
    # 2: Group: first enemy starts spawning, then 2nd enemy once 1st enemy is done, etc. (125% spawn speed, 2sec between groups)
    # 3: Mixed group: all enemies spawn rapidly for a few seconds (2.5x rate for 5sec) then stop spawning for a few seconds (5sec)
    formation = 1  # random.randint(0, 3)
    
    # choose enemies
    outputWave = [[random.choice(list(valueList))] for i in range(numEnemies)]

    for i in range(numEnemies):
        # split the total power into each enemy
        strength = powerTotal / numEnemies
    
        if formation == 2:  # group
            pass
        if formation == 3:  # mixed group
            pass
        else:  # regular, default
            num = round(strength/valueList[outputWave[i][0]], 0)
            delay = random.uniform(0, 1)
            interval = valueList[outputWave[i][0]] / (powerRate/numEnemies)
            outputWave[i] = [outputWave[i][0], num, delay, interval]

    print("WAVE ",wave, ":", outputWave)
    return outputWave
    
