# shapeDefense
simple tower defense test; may be moved to unity after


FOR CHANGING DATA FILES:

MAPS:
The game is 20x15 tiles. The start and end tiles should be off screen (so 0 or 21 for x, 0 or 16 for y)
the first two sets of integers defines the colour scheme
Upon reading "spawns", the coordinate values indicate entrances and their respective exit
Upon reading "obstacles", the coordinate values indicate blocked places, as a rectangle (x, y, length, height)

EXAMPLE:
220 240 120 // background colour, do not make any values less than 20
230 200 110 // path colour
spawns
0 2 21 2    // start and exit
obstacles
2 3 3 6     // 2x4 rectangle obstacle

The resulting map would look like this:
S---------------------E

  OO
  OO
  OO
  OO

TOWERS:
Booster towers grant bonuses to adjacent turrets.
Turrets fire projectiles to damage enemies

General attributes:

name        // name of the tower, this should always be first
type        // booster or turret
cost        // cost for purchase, selling price is half of this + upgrades
sprite_base // this sprite does not rotate

Turret attributes:
damage INT      // damage per projectile, reduced by 1 per armour point.
rate FLT        // rate of fire per second
range FLT       // range in # of tiles (x50 for pixels)
proj_spd FLT    // tiles per second
up_cost             // upgrade cost
up_cost_inc    // increase in upgrade cost for every additional upgrade
max_level           // level starts at 1 and increases by 1 every upgrade, a low max level can prevent all upgrades from being purchased
sprite_turret   // rotating turret on top of the base sprite
sprite_proj     // the sprite of the projectile it shoots
hit_sound       // sound the projectile plays when hitting an enemy
targeting       // 0 = doesn't attack, 1 = ground only, 2 = air only, 3 = air and ground

Booster tower attributes:
boost_type STR // what stat to boost (damage, rate, range, proj_spd)
boost_value INT // % of the stat to boost, stacks additively with other boosters

the last line should always be:
end


ENEMIES:

name
type  // "BOSS" (10 damage, rarer) or "NORMAL"
movement_type  // "GROUND" or "FLYING", increases slowly over time
health  // hitpoints, increases over time
regeneration  // hitpoint regeneration per second, increases slowly over time
armour  // each point of armour reduces incoming damage by 1, increases slowly over time up to double
speed  // in tiles per second, increases very slowly over time up to 1.5x
death_spawn_enemy  // name of the enemy that spawns when this one dies, 'none' means it doesnt spawn any
death_spawn_val  // how many are spawned
bounty  // how much gold u get from killing it, can be a float, in which case it will randomize. Increases over time up to double.
sprite  // sprite of the enemy
radius  // radius of the enemy for tower range and detection. Projectile hits use a mask.
end


WAVES:
Enemies grow stronger with each wave.
calculations for stats that increase, with x indicating the base amount and t indicating number of waves completed:
Health [NO MAX]: x * (1 + t / 10)           // increases by  flat  10% per wave. No max. This changes to 20% after wave 50.
Regeneration [MAX 3x]: x * (1 + t / 25)     // increases by a flat 4% per wave, maxes out after 50 waves
Armour [MAX 2x]: x * (1 + t / 50)           // increases by a flat 2% per wave, maxes out after 50 waves
Speed [MAX 1.5x]: x * (1 + t / 100)         // increases by a flat 1% per wave, maxes out after 50 waves.
Bounty [MAX 2x]: x * (1 + t / 50)           // increases by a flat 2% per wave, maxes out after 50 waves

waves file:

wave + an integer indicates the wave
Syntax for one wave:

name_of_enemy
amount separation start_time

name_of_enemy: name of the enemy spawning, based on the enemyData file
amount: how many to spawn. If there are multiple spawn points, enemies will alternate spawn locations
separation: time, in seconds, between two of the enemies spawning. For example, if amount = 3 and separation = 1. It will spawn an enemy at 0,1,and 2 seconds
start_time: time, in seconds, when to start spawning this enemy after the wave begins.

For example:

// wave one: spawns 5 brutes over 8 seconds, 3 seconds in, spawns 20 common circles over 19 seconds, 5 seconds in, spawns 10 fling over 9 seconds
wave 1
brute
5 2 0
common circle
20 1 3
common flying
10 1 5

// wave two: spawns 10 assault enemies, with 0.75sec separating spawns
wave 2
assault
10 0.75 1

