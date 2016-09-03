from z3 import *

a = Int('a')
b = Int('b')

s = Solver()
s.add((ord('T')*a+b)%251 == 0x80)
s.add((ord('W')*a+b)%251 == 0x5e)
s.add((ord('C')*a+b)%251 == 0xed)
s.add((ord('F')*a+b)%251 == 0xcb)

s.check()
m = s.model()

a1 = m[a].as_long()
b1 = m[b].as_long()

decr = [(i*a1+b1)%251 for i in xrange(256)]

b = "805eed80cbbccb94c36413275780ec94a857dfec8da8ca94a8c313a8ccf9"

o = ""
while b:
	t = int(b[:2],16)
	b = b[2:]

	o += chr(decr.index(t))

print o
