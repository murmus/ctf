from pwn import *

buf = open('prog').read()

warry = []

while buf:
	word = u16(buf[:2])
	warry.append(word)
	buf = buf[2:]

w0 = 0
w1 = 0
w2 = 0
pc = 0

output = ""

verbose = False

def put(char):
	global output
	global verbose

	output += "%c" % char
	if verbose:
		print output
	if len(output)>0x20:
		output = output[1:]

buf = open("dmp").read()

def get():
	print "To write: '%s'" % repr(buf[:20])
	global buf
	global verbose

	b = buf[0]
	buf = buf[1:]

	if buf[:4] == "aaaa":
		verbose = True
		f = open("memdmp2",'w')
		for byte in warry:
			f.write(p16(byte))
		f.close()
		print "MEMORY DUMPED"
	return ord(b)

while 1:
	w0 = warry[pc]
	w1 = warry[pc+1]
	w2 = warry[pc+2]
	if verbose:
		print "pc[%04x]:\tw0 %04x\tw1 %04x\tw2 %04x" % (pc,w0, w1, w2)

	if pc == 0xc9:
		f = open("memdmp",'w')
		for byte in warry:
			f.write(p16(byte))
		f.close()
		print "MEMORY DUMPED"
	if w0 == 0xffff and w1 == 0xffff:
		print "IO DIE"
		exit(0)
	if w0 < 0xffff:
		if w1 < 0xffff:
			if verbose:
				print "Sub %04x-=%04x" % (warry[w1],warry[w0])
			warry[w1] -= warry[w0]
			if warry[w1]<0:
				warry[w1] += 0x10000
			if verbose:
				print "  = %04x"% (warry[w1])
			
			if warry[w1] > 0 and warry[w1] <0x8000:
				pc += 3
			else:
				pc = w2

		else:
			if verbose:
				print "Put %x" % (warry[w0])
			put(warry[w0])
			pc += 3
	else:
		print "Get idx=%x" % (w1)
		warry[w1] = get()
		if warry[w1] >0 and warry[1] <0x8000:
			pc +=3
		else:
			pc = w2
