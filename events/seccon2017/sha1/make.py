a = open("shattered-1.pdf").read()[:0x140]
b = open("shattered-2.pdf").read()[:0x140]

a += "Q"*1024*2017
b += "Q"*1024*2017

open('s1.pdf','w').write(a)
open('s2.pdf','w').write(b)
