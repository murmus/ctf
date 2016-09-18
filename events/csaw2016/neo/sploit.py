import requests
import base64

valid ="aEzJIJlNoSmcPfymefnCBsTLNakMFdhn/hYxBe1IM1HN8rb9h8hmeRMei8Ku6fmD1vIW7IetHyrLoK6JpzoGKwGchzOMmQirNAxjD9Lr3SA="
r = requests.post("http://crypto.chal.csaw.io:8001/",data={'matrix-id':valid})
data = base64.b64decode(valid)

correct = r.text

'''
i2[16] = 37 ^ 1 = 36
i2[15] = 11 ^ 2 = 9
'''
dec = ""
while data:
	c1 = data[-32:-16]
	t = []
	#t = [171, 253, 25, 227, 136, 162, 16, 37, 196, 175, 161, 134, 168, 53, 9, 36]
	for i in xrange(16):
		known = "".join([chr(i^(len(t)+1)) for i in t])
		got = False
		for i in xrange(0x100):
			test = "A"*(15-len(known))+chr(i)+known
			part = test + data[-16:]
			r = requests.post("http://crypto.chal.csaw.io:8001/",data={'matrix-id':base64.b64encode(part)})

			print r.text == correct
			if r.text == correct:
				print i ^ (len(known)+1)
				got = True
				break
		assert(got)
		t = [i ^ (len(known)+1)]+t
		print t, repr(dec)

	dec = "".join([chr(ord(c1[i])^t[i]) for i in xrange(16)]) + dec
	print repr(dec)
	data = data[:-16]
