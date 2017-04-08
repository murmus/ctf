from pwn import *

s = process("./crcme_8416479dcf3a74133080df4f454cd0f76ec9cc8d")
s.clean()

crcs = {}
for i in xrange(0x100):
	if i in []:
		continue
	s.sendline("1")
	s.sendline("1")
	s.sendline("%c" % i)
	print i
	s.recvuntil("is: ")
	crc = s.recvline()

	crcs[int(crc,16)] = i
	s.clean()
	print i

import pickle
pickle.dump(crcs,open('crclookup','w'))
