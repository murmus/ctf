from pwn import *

s = remote("misc.chal.csaw.io",8001)

s.recvline()

num = 0
while 1:
	num += 1
	reg = s.recvline()[:-1]
	if reg == "Irregular":
		print "shit"
		break

	out = ""
	while reg:
		last = ""
		print num, reg
		if reg and reg[0] == "\\":
			if reg and reg[1] == "D":
				out += "A"
			if reg and reg[1] == "W":
				out += " "
			if reg and reg[1] == "w":
				out += "A"
			if reg and reg[1] == "d":
				out += "9"
			last = out[-1]
			reg = reg[2:]
		if reg and reg[0] == "[":
			if reg[1] == "\\":
				if reg and reg[2] == "D":
					out += "A"
				if reg and reg[2] == "W":
					out += " "
				if reg and reg[2] == "w":
					out += "A"
				if reg and reg[2] == "d":
					out += "9"
				last = out[-1]
			else:
				out += reg[1]
				last = out[-1]
			reg = reg[1+reg.index("]"):]
		if reg and reg[0] == "(":
			t = reg[1:reg.index(")")]
			if reg and t.count("|"):
				last = t[:t.index("|")]
			else:
				last = t
			out += last
			reg = reg[reg.index(")")+1:]

		if reg and last == "":
			last = reg[0]
			reg = reg[1:]
			out += last

		if reg and reg[0] == "+":
			reg = reg[1:]
		if reg and reg[0] == "*":
			reg = reg[1:]
		if reg and reg[0] == "{":
			t = reg[1:reg.index("}")]
			if reg and t.count(","):
				count = int(t[:t.index(",")])
			else:
				count = int(t)
			out += last*(count-1)
			reg = reg[reg.index("}")+1:]
		

	s.sendline(out)
