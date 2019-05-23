# shapeDefense
simple tower defense test; may be moved to unity after

Long ago, the shapes lived in peace and harmony, but it all changed when the circles attacked!
Only the player, master of all the shapes, may defeat them. :)

In this tower defence you place down towers which can simultaneously defend as well as change the path that enemies follow.
Money is earned by killing enemies and at the end of each round, which can be used to buy and upgrade towers.
Wave will get progressively harder: Enemies will be more numerous and also gain strength each passing wave.
Defend for as long as you can! (currently only 30 waves)

read modding_info.txt if you would like to change around the stats of various towers (WIP)

TODO:
- Separate the 'special' tags of towers into two different tags that determine how the towers hit enemies ('targeting'), and the effect of the hit on enemies (hit_special) (e.g. the freezer tower would become "aura" and "slow" instead of "AOE_slow"). Targeting will have one special value associated with it, hit_special will have up to two values.

'target' tags:
- projectile (regular gun); no special value
- exploding_projectile (projectile with AOE); special value for radius of explosion
- piercing (shots pierce enemies); special value is how many enemies they can hit
- aura (area of effect centered on tower); no special value, the area of effect is equal to the tower's range.

'hit_special' tags:
- none; no effect, only damage. This is the default if no tag is specified
- slow; slows enemies and also reduces health regeneration
- weakness;


