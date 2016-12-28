import dpkt
import base64

def decode_b32(s):
	s = s.upper()
	for i in range(0x10):
		try:
			return base64.b32decode(str(s))
		except Exception as e:
			s += '='
	raise ValueError('Invalid base32')

last_s = ""
last_c = ""
full_c = ""

gpg = ""
file_pieces = []
inf = False
for ts, pkt in dpkt.pcap.Reader(open("dump.pcap")):
	#print ts, repr(pkt)
	eth = dpkt.ethernet.Ethernet(pkt)
	dns = dpkt.dns.DNS(eth.data.data.data)

	assert len(dns.qd)==1
	buf = "".join(dns.qd[0].name.split(".")[:-2])
	s =  decode_b32(buf)[6:]
	if s != last_s:
		print "-->", repr(full_c)
		print repr(s)
		if full_c.count("BEGIN PGP PUBLIC"):
			gpg = full_c
		if s.count("START_OF_FILE"):
			inf = True
		if inf and s not in file_pieces:
			file_pieces.append(s)
		if s.count("END_OF_FILE") and not s.count("START_OF_FILE"):
			inf = False
		last_s = s
		full_c= ""
	if dns.an:
		assert len(dns.an)==1 
		resp = "".join(dns.an[0].cname.split(".")[:-2])
		c = decode_b32(resp)[6:]
		if c != last_c:
			last_c = c
			full_c += c

open("gpg.dmp",'w').write(gpg)

secret = "".join(file_pieces)
secret = secret[len("start_of_file"):-len("end_of_file\n")]
open("secret.docx",'w').write(secret)
