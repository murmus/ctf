from pwn import *

def isPrime(Number):
    return 2 in [Number,2**Number%Number]


for i in xrange(0x756000, 0x756200):
	if isPrime(i):
		print hex(i)
