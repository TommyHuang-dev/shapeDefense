# shapeDefense
simple tower defense test; may be moved to unity after

MAP FILES:
The game is 20x15 tiles. The start and end tiles should be off screen (so 0 or 21 for x, 0 or 16 for y)
contains a set of x y coordinates for every corner, separated by a space.
The first coordinate is the start and the last is for the end.

EXAMPLE:
0 2   // start
4 2   // corner
4 5   // corner
21 5  // end

The resulting map would look like this:
S----
    -
    -
    -----------------E

