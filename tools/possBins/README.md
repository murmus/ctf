possBins uses Binary Ninja (https://binary.ninja/) and Manticore (https://github.com/trailofbits/manticore) to determine if a given binary can make allocations (by dlmalloc, the glibc implementation) that would be put into the fastbins, smallbins, largebins, or mmap'd regions when freed.

The rough process is:

* Using binary ninja:
 * patch out some of the libc function calls that are common and we don't care about, but trip up manticore:
  * alarm, setvbuf, things like that.
 * Also using binary ninja, find all the calls to malloc and what the arguments to it are.
 * If the argument is not concrete, add that call to the list of analyses for manticore.
* Using manticore:
 * Take the list of malloc calls and attempt to solve for the various bin sizes
