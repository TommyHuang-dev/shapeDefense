import random

valueList = {}  # list of [['enemy name', cost], [...]].
# enemyValues file contains the base "cost" to spawn enemies. Higher cost = stronger enemy = less.
# additionally spawning enemies with less delay in between also costs more (default = 1sec)
with open("data/enemyCost", "r") as f:
    for line in f:
        if len(line.strip()) != 0:
            newLine = line.strip().split()
            cost = float(newLine[-1])
            del(newLine[-1])
            name = ' '.join(map(str, newLine))
            valueList[name] = cost

# outputs a new random wave with format: [['name', num, delay, interval], ['speedy', 12, 2.0, 0.75]]
def generate(wave):
    # powerTotal is the total strength of the spawned enemies
    # powerRate is the rate they spawn
    # power total and power rate are inversely correlated
    powerRandom = random.uniform(-0.2,0.2)  # make total power and rate inversely related
    
    # TODO rescale this
    powerTotal = 12 * (wave ** 1.2) * (1 + powerRandom)
    powerRate = 4 + 0.7 * wave * (1 - powerRandom)
    
    # number of different enemy types to spawn
    numEnemies = random.randint(3, 5)

    # some waves have a larger variety of enemies and more of them
    if wave % 20 == 0:
        numEnemies += 2
        powerTotal *= 1.4
        powerRate *= 1.2
    elif wave % 5 == 0:
        numEnemies += 1
        powerTotal *= 1.2
        powerRate *= 1.1
    
    # Formation is how they will spawn (e.g. in groups, or just regularly):
    # 0,1: Regular 
    #   all enemies start spawning at beginning and spawn at uniform intervals.
    #   spawn rate is divided among enemies
    # 2: Group
    #   first enemy starts spawning, then 2nd enemy once 1st enemy is done, etc. 
    #   2 seconds between groups
    # 3: Staggered
    #   Similar to regular, but groups start spawning with a small staggered interval
    #   spawn rate is divided among enemies, but has a small boost
    formation = random.randint(0, 3)
    outputWave = [[random.choice(list(valueList))] for _ in range(numEnemies)]
    totalTime = 0
    for i in range(numEnemies):
        strength = powerTotal / numEnemies
        if formation == 0 or formation == 1:  # regular
            num = round(strength / valueList[outputWave[i][0]], 0)
            delay = random.uniform(0, 2)
            interval = valueList[outputWave[i][0]] / (powerRate / numEnemies)
        elif formation == 2:  # groupsed
            num = round(strength / valueList[outputWave[i][0]], 0)
            delay = random.uniform(0, 1) + totalTime
            interval = valueList[outputWave[i][0]] / powerRate
            totalTime += interval * (num - 1) + 2
        else:  # staggered
            num = round(strength/valueList[outputWave[i][0]], 0)
            delay = 3 * i + random.uniform(0, 1)
            interval = valueList[outputWave[i][0]] / (powerRate * 1.1 / numEnemies)
        
        outputWave[i] = [outputWave[i][0], num, delay, interval]

    return outputWave
    
