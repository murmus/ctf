f = open("tutorial")
a = f.read()
f.close()

offset = a.index("\xE8\x00\xF9\xFF\xFF")
assert a.count("\xE8\x00\xF9\xFF\xFF")==1
noalarm = a[:offset]+"\x90"*5+a[offset+5:]

offset=a.index("\xE8\x39\xFB\xFF\xFF\x89\x45\xcc")
assert a.count("\xE8\x39\xFB\xFF\xFF\x89\x45\xcc") == 1
nopriv = noalarm[:offset]+"\x90"*5+noalarm[offset+5:]

open("tutorial_",'w').write(nopriv)
