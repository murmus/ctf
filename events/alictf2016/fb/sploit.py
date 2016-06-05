from pwn import *

s = process("./fb_noalarm")

def alloc(i):
	s.sendline("1")
	s.sendline("%d" % i)
	s.recvuntil("Done~")
	s.recvuntil("Choice:")

def setmsg(i,buf):
	s.sendline("2")
	s.sendline("%d" % i)
	s.sendline(buf)
	s.recvuntil("Done~")
	s.recvuntil("Choice:")

def delmsg(i):
	s.sendline("3")
	s.sendline("%d" %i)
	s.recvuntil("Done~")
	s.recvuntil("Choice:")

