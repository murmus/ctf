Another simple stack buffer overflow, this time with **gets** onto the stack...

The trick, though, is there are stack cookies.

For a leak, we use the crc function to give us the crc of a single byte at a time. Since I didn't feel like reversing it/porting it to python, I decided to just make a single byte lookup table and use that (see gencrc.py).

Using that and a pointer overwrite as an arbitrary read, we leak out the stack cookie, then some got values to find their libc in libc-db (niklasb's variant), and then it's just a ret-to-libc system("/bin/sh").

Note: there was some stability problems while I was trying to throw this, kill connections very quickly, so I commented out some of the reads to make it go faster.
