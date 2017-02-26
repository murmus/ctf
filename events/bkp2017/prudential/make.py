import urllib

a = open("shattered-1.pdf").read()[:0x140]
b = open("shattered-2.pdf").read()[:0x140]

print urllib.urlencode({"name":a, "password":b})
