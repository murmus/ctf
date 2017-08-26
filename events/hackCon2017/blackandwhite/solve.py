from PIL import Image

im = Image.open("image.png")
pix = im.load()

pi = []
for y in xrange(96):
	for x in xrange(96):
		pi.append(pix[x,y])

f = open("out",'w')
for c in pi:
	f.write(chr(c>>8))
	f.write(chr(c&0xff))

