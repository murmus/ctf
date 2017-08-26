from PIL import Image

im = Image.open("Secret.png")
pix = im.getdata()
mode = len(im.mode)

out = ""
t = ""
for i in xrange(len(pix)):
	t += "%d" % (pix[i][i % mode]&1)
	if len(t) == 8:
		out += chr(int(t,2))
		t = ""

print out
