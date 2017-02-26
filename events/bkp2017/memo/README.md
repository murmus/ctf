Pretty simple heap buffer overflow. Overflow into a free'd fastbin sized allocation. Note that we have to set up one of the sizes right to make the eventual malloc into the bss work.

After that, every edit will write over all the pointers, we do it once to point the memos[2] to the `__free_hook`, then the second time to make it system.
