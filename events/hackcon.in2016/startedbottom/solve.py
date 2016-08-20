from z3 import *

s = Solver()

x = BitVec('x',32)
s.add(x==0xdeadbeef)

xs = [x]
vs = []
for i in xrange(10):
	xs.append(BitVec("x%d"%i, 32))
	vs.append(BitVec("v%d"%i, 32))

	s.add(vs[i]>0x30)
	s.add(vs[i]<0x7f)
	s.add(xs[i+1] == xs[i]*8+vs[i])
	
s.add(xs[i+1] == 0xcafebabe)
s.check()

m = s.model()

out = ""
for i in xrange(len(vs)):
	out += chr(m[vs[i]].as_long())

print out+"\x00"
