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
- chain [NEW] (targets the nearest enemy and continually damages it); special value determines how many times it will leap to a new target.

'hit_special' tags:
- none: no effect, only damage. This is the default if no tag is specified
- slow: slows enemies by a percentage and reduces health regeneration slightly (half the percentage). Special values determine the magnitude of the slow and how long it lasts for. If multiple slows are on a enemy, only the biggest one applies.
- poison [NEW]: deals damage over time to enemies and removes all health regeneration. Special values determine damage per second and the duration in seconds. Only the largest poison applies.
- fire [NEW]: deals high damage over time, but cancels out slowing effects. Special values determines damage per second and duration in seconds. Only most intense fire applies.
- weakness [NEW]: increases damage dealt to enemy after armour reductions. Special values determine the percentage bonus and duration. Only one weakness can apply.
- ignore_armour [NEW]: this tower's attacks ignore a percentage of armour on enemies. If the number is greater than 100% then it will do bonus damage against enemies with armour.
