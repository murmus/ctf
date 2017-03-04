Time_machine was interesting. It's a binary that has encrypted most of their functions with an xor, and they get decrypted just before calling. I'm planning on doing some more about how to solve this with Binary Ninja, and I'll come back and edit this when I do.

As far as the exploit: I attempt to log in as the specified flag user. This reads the password for the user into the heap. I then register a new username and log into it. Once logged in, the "Get Boarding Pass" function has a format string bug in it, although it looks like %n is disabled, althouhg I didn't investigate too much.

In any case, I set it up once to leak out a heap pointer via %<idx>$p, then print out the flagid password from the heap. After that it's just a matter of logging out and loggin back in as the flagid and getting a voucher with a flag.
