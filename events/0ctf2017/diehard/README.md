They're using some non-dlmalloc allocator for heap allocations. I'm not entirely sure how it works, but they have a hardcoded handler for if I submit a message greater than 2016 bytes. While I was playing with that, I noticed I could get it to return the same pointer multiple times when messing with buffers that are 2015 bytes in length. 

In any case, this writes 2 messages of length 2015, then one of 2017 which blows away the structure of the second 2015. I use that to read out a got pointer, free that, and blow away the same buffer a second time to hit the bespoke gadget.

Given the flag (flag{W33_g0t_H34p_me7ad4t4_!n_BSS}), I suspect this was _not_ the intended solution.
