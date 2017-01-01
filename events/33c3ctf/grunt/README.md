I didn't manage to complete this during the competition, so everything is based off my local system and libc. I also didn't fix it to work remotely, so you'd have to fix that to to reproduce.

The challenge was a lua "game" which does "pokemon" fighting. Figuring things out mostly ended up being reversing the lua game and understanding how the c bindings work. The bug (at least that I used), was that the incapacitate attack didn't check if there was an attack before removing it.

To exploit this, we modify the "Airmackly" pokemon to have 2 incapacitate attacks, in the "c" function. This function gets called during the first round of combat due to the call at line 14. We do this by dealing some damage (just to prove it works), then swapping the first and second attacks and duplicating the (new) second attack into the third slot.

Any combat with Airmackly, if there is only one attack on a pokemon, is to now have 0xff attacks. This means that we can call both getAttack and swapAttack with values up to 0xff.

The lua heap though, is a little confusing. I never figured out a good way to groom it, so this exploit basically just sprays a vulnerable state around. We create 100 pokemon that have 0xff attacks, then scan through the 250 addressable attacks (technically it should be 255 attacks, but I rounded because I didn't want to figure out the off-by-one part. Lua being one indexed hurts my head).

This scanning is done from lines 49 to 73. there are a few index variables we use: a and b, which tell us where we found magic values. a becomes the index for 0x626098, the got entry for memset which we are bashing. b is the index for the "damage" field of another pokemon. The other variables should be fairly straightforward: d is the index for the second pokemon we are going to bash.

finally, at line 63 we go through and actually get an exploitable state. we swap the 0x626098 address with the name field of the ps[d] pokemon. Then, we get the name for ps[d], convert that to an integer, and subtract 0x12cc9f0 (the offset to system, on my libc). we write it back, and use the "Andyball" pokemon to use the amnesia attack to use memset to remove the pokemon name. Since we set that pokemon up to be "/bin/sh", this pops us a nice shell.
