# shapeDefense
simple tower defense test; may be moved to unity after


FOR CHANGING DATA FILES:

MAPS:
The game is 20x15 tiles. The start and end tiles should be off screen (so 0 or 21 for x, 0 or 16 for y)
The first integer determines the difficulty of the map (1 = easy, 2 = medium, 3 = hard)
The next two sets of integers determines the colour theme of the map (RGB values for grass and path)
Afterwards, it contains a set of x y coordinates for every corner.
The first coordinate is the start and the last is for the end.
When reading "obstacles", the next set of coordinates will be placed in a different list

EXAMPLE:
2       // medium difficulty
220 240 120 // grass colour, do not make any values less than 20
230 200 110 // path colour
0 2     // start
4 2     // corner
4 5     // corner
21 5    // end
obstacle
2 2
5 2

The resulting map would look like this:
S----
  o -o
    -
    -----------------E


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
