"Simple" heap overflow.

I allocate 3 buffers of size 0xff, the use the unlimited overflow to double the size of the second.

Free that double size buffer, and allocate 2 more 0xff buffers.

Now allocations g and j in the script overlap. I free j and k so that j will have pointers to main_arena (due to the consolidation triggered by k).

Then the tricky part: I allocate 4 0x2f buffers, and free b and c. I found a 0x40 sitting in the data section, so I use that as the size for a fastbin unlink, allocate two new 0x2f buffers, the second of which is going to be in the data section. Finally, I use that to drop a bespoke gadget into the malloc_hook, and then make one finall allocation to pop a shell.
