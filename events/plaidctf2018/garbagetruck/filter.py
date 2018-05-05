from pwn import *

def isPrime(Number):
    return 2 in [Number,2**Number%Number]

'''
s = process("./garbagetruck_04bfbdf89b37bf5ac5913a3426994185b4002d65")

for i in xrange(1, 108):
	if isPrime(i):
		s.sendline("%d" % i)

s.clean(1)

s.interactive()
'''

fi = open("gadgets").readlines()

out = open("filtered",'w')
print len(fi)
count = 0
for l in fi:
	q = int(l[l.index("0x"):l.index(":")-4], 16)
	count += 1
	if isPrime(q):
		out.write(l)

out.close()
