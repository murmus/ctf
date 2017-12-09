from PIL import Image
import os

orig = open("tktk-892009a0993d079214efa167cda2e7afc85e6b9cb38588cba9dab23eb6eb3d46").read()

html = "<html><body>"
count = 0
for i in xrange(len(orig)):
	for j in xrange(8):
		buf = list(orig)
		buf[i] = chr(ord(buf[i]) ^ (1<<j))
		fname = "ims/i-%d-%d.jpg" % (i,j)
		open(fname, 'w').write("".join(buf))
		try:
			im = Image.open(fname)
			im.crop((0,0,1,1))
			html += "<img src=\"ims/i-%d-%d.jpg\">\n" % (i,j)
			count += 1
			print count
		except:
			os.remove(fname)

html += "</body></html>"
open("reader.html",'w').write(html)
