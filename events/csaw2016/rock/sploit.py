from pwn import *
import time

base = ""
for j in xrange(30):
	for i in xrange(0x31,0x100):
		s = process("./rock")
		string = base+chr(i)
		string += "A"*(30-len(string))
		s.sendline(string)

		buf = s.recvall()

		if not buf.count("You did not pass %d" % j):
			print buf
			print string
			time.sleep(1)
			break
	base += chr(i)
