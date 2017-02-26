from pwn import *

count = 0
while 1:
	try:
		s = remote("54.202.7.144",9875)
		#s = process("./sss")

		s.recvuntil(">_")
		def sign(com):
			s.sendline("1")
			s.recvuntil(">_")
			s.sendline(com)
			buf = s.recvuntil(">_")
			if buf.count("signature"):
				out = buf.split("\n")[1]
			else:
				out = None

			return out
		def execc(com,sig):
			s.sendline("2")
			s.recvuntil(">_")
			s.sendline(com)
			s.recvuntil(">_")
			s.sendline(sig)
			return s.recvuntil(">_")

		sig = sign("ls")
		com = "echo \"A\"\"B\"\"C\";cat flag;"
		com += randoms(255-len(com))
		buf = execc(com, "A")

		count += 1
		if buf.count("wrong"):
			print "Failed", count
		else:
			print (com)
			print buf
			if buf.count("ABC"):
				break
	except:
		count += 1
		print "FAILED", count
