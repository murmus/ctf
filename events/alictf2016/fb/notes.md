single null-byte heap overflow with no pointer leak but no PIE.

Uses the null byte overflow to use coallescing to unlink into the BSS where a known pointer exists.

Once that's done, uses the program functionality to bash free pointer->puts, and uses that to leak memory.

Tried several different things at this point (see commmented out code), eventually just used niklasb's libc-database to find their libc and do system("/bin/sh") that way.

Note the code for DynELF: it works local, and seems to work remote, but even from EC2 the connection was too slow to make it finish.
