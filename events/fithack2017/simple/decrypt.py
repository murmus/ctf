import binascii

key = "J2msBeG8"
enc = open("enc_mes.txt").read()
enc_mes = binascii.unhexlify(enc)

dec = ["0"]*(len(enc_mes))


for i in xrange(len(dec)):
	dec[i] = chr(ord(enc_mes[i])^ord(key[i/(len(dec)/len(key))]))

out = ""

i = 0
while len(out)<len(dec):
	out += dec[i]
	i += len(dec)/len(key)
	if i>=len(dec):
		i += 1
		i %= len(dec)

print out
