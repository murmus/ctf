This one is a little messy. There's a one-byte overflow when reading in your commands, so we're able to swap from md5 to sha1 after it has decided to use the space for the md5.

This leads to a one-byte overflow in the sha1 computed, overwriting the low byte of the deny command function. This just brute forces getting it to be exec, instead.
