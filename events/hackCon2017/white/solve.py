from PIL import Image
import base64
magic = base64.b64encode("\x89PNG")[:5]

buf = open("final.png").read()
ou = Image.new("RGB", (170,170), (255,255,255))


i = 0
while 1:
	# iVBOR is png header base64d
	open("out-%d.png" % i, 'w').write(buf)
	
	im = Image.open("out-%d.png" % i)
	x = (i % 6) * 27
	y = (i/6) * 34

	ou.paste(im, (x,y))

	if magic not in buf:
		break
	buf = buf[buf.index(magic):]
	buf = base64.b64decode(buf)
	print "Solved another, now %d len" % (len(buf))
	i += 1

ou.save("out.png")
