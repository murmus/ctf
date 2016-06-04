check = []
t = 0
for i in xrange(1,100):
	t += i
print "Check1: +%d" % (t)
check.append(t)

t = 0
for i in xrange(1,1000):
	t += i
print "Check2: +%d" % (t)
check.append(t)

t = 0
for i in xrange(1,10000):
	t += i
print "Check3: +%d" % (t)
check.append(t)

i = 99
t = 0
while (i-1)>0:
	q = i*2%3
	i -= 1

	if q == 0:
		t += check[0]
	if q == 2:
		t += check[2]
	if q == 1:
		if (i%2):
			t -= check[1]
		else:
			t += check[1]

print "Modified %d" % t
ans = 1835996258
a3 = ans-t
print "ans      %d" % ans
print "Solved   %d" % (a3)


v3 = a3 / 1000 % 10;
v4 = a3 / 10000 % 10;
v5 = a3 % 10 & 0xFF;
v10 = v3 + a3 % 10 * v4;
v6 = a3 / 1000000 % 10 & 0xFF;
v7 = a3 / 100 % 10 & 0xFF;
v11 = v4 * v6 + 10 * v7 + 3;
v12 = 10 * (v3 + v4);
v13 = v4 * v6;
v14 = 19 * (a3 / 100000 % 10) + 2;
v15 = v5 * v6 + 1;
v16 = v5 * v6;
v17 = 12 * v7;
v19 = 12 * v7 + 3;
v18 = 10 * (v3 + v4) + v3;
v20 = 2 * (v4 * v6 + 10 * v7 - 37);

print "alictf{%s}" % ("".join([chr(i) for i in [v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20]]))
