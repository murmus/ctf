Another simple one: stack based buffer overflow.

I had to swing around twice: the first time leaks out the address of atoi by using printf, we then start the program over again and do system("/bin/sh;#").
