Whew. Same as start, but with NX turned on.

What I ended up with was kind of gross.

* Ripped libc off the original start box
* first set of gadgets sets up a read(0,read@plt,0x400)
* write a single byte (0xd0) to change read@plt to write
* gadget so rsi = 1 (stdout)
* write(1, plt, 0x400)
* use a pop rbp, ret gadget to load rbp with an arbitrary address
* use the saving off of argv in main to re-write the low byte of read@plt to read
* use that call to read to demolish the data section

* use a bunch of rop-nops to make it so that system will have enough space for it's calls

* call system(/bin/sh)
