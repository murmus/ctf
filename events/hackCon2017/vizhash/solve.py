from PIL import Image
import hashlib
import math
import base64

im = Image.open("digest.png")
pix = list(im.getdata())

lookup = []

for i in xrange(256):
	m = hashlib.md5()
	m.update(chr(i))
	m = m.hexdigest()
	m = int(m,16)
	m = str(hex(m))

	q =  ""
	for j in range(0, len(m)-3, 3):
		q += chr(128+ord(m[j])^ord(m[j+1]))
		q += chr(128+ord(m[j+1])^ord(m[j+2]))
		q += chr(128+ord(m[j+3])^ord(m[j+2]))

	lookup.append(q)

buf = ""
for i in xrange(0, len(pix), 11):
	q = ""
	for j in xrange(11):
		q += chr(pix[i+j][0])
		q += chr(pix[i+j][1])
		q += chr(pix[i+j][2])

	if q not in lookup:
		break
	buf += chr(lookup.index(q))

c = len(buf)
clen = math.floor(math.sqrt(c*2))

cryptd = buf[int(0-clen):]

ptext = "".join([chr(ord(c)-4) for c in cryptd[::-1]])

print base64.b64decode(ptext)
