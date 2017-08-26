def rot13(st):
	mod = [chr(i+0x61) for i in range(27)]
	out = ""

	for c in st:
		i = ord(c)-0x61
		i = (i+13)
		if i >len(mod):
			i -= len(mod)-1
		out+= mod[i]
	return out

goal = "firhfgferfibbqlkdfhh"

buf = rot13(goal)

out = ""

for c in buf:
	out += "%02X" % (ord(c))
print out
