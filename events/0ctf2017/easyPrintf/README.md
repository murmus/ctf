printf vuln.

you are allowed to print out an arbitrary address, then you're give a little over 150 bytes of format string to work with. It's also full relro, so no just bashing the got.

I'm super curious how other teams solved this. Our solution was to bash the malloc_hook in libc with system, write "/bin/sh" into the bss, and then trigger a malloc(addrBinsh) using a format specifier.

