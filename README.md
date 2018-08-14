# shapeDefense
simple tower defense test; may be moved to unity after

MAP FILES:
The game is 20x15 tiles. The start and end tiles should be off screen (so 0 or 21 for x, 0 or 16 for y)
The first integer determines the difficulty of the map (1 = easy, 2 = medium, 3 = hard)
The next two sets of integers determines the colour theme of the map (RGB values for grass and path)
Afterwards, it contains a set of x y coordinates for every corner.
The first coordinate is the start and the last is for the end.

EXAMPLE:
2       // medium difficulty
220 240 120 // grass colour, do not make any values less than 20
230 200 110 // path colour
0 2     // start
4 2     // corner
4 5     // corner
21 5    // end

The resulting map would look like this:
S----
    -
    -
    -----------------E

Tower data files:
Every tower needs three sprites, a base and a rotating turret, and a bullet
It also needs a sound file when the projectiles hit an enemy.
Attributes:
name        // name of the tower
damage      // damage per shot
rate        // rate of fire per second
volley      // number of shots
area        // for volley > 1, how spread out the shots are
range       // range, in number of tiles
proj_spd    // projectile speed of the shot, in tiles per second
piercing    // how many enemies one shot can hit
special     // special effect (e.g. slowing enemies)
special_val // value for the special effect
upgradeA1   // top upgrade
upgradeA2   // top upgrade 2
sprite_base     // base sprite
sprite_turret   // turret sprite
sprite_bullet   // bullet sprite
hit_sound       // sound played on hit
