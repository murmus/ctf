Super simple buffer overflow.

I tried using the shellcraft stuff from pwntools, couldn't get it to work. Used some simple ROP to read into BSS (since I don't know where the stack is), then just ret to that. Shellcode from shellstorm.
