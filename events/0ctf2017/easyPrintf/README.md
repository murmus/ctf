printf vuln.

you are allowed to print out an arbitrary address, then you're give a little over 150 bytes of format string to work with. It's also full relro, so no just bashing the got.

I'm super curious how other teams solved this. Our solution was to bash the malloc_hook in libc with system, write "/bin/sh" into the bss, and then trigger a malloc(addrBinsh) using a format specifier.


Other writeups:

* https://gist.github.com/Laxa/8b6b137e7e5e232d0764b4f048584ba6
* http://blog.dragonsector.pl/2017/03/0ctf-2017-easiestprintf-pwn-150.html
* Someone in IRC said they used https://www.gnu.org/software/libc/manual/html_node/Printf-Extension-Example.html#Printf-Extension-Example
