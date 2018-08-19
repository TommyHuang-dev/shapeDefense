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


CORES (WIP):
Equipped by turrets to boost stats or change their attack. Each turret can equip one.
Potential cores:
Sniper
Machinegun
Flak
Cryo
Cannon

Attributes:
name
cost
effect_name
effect_val
