f = open("tutorial")
a = f.read()
f.close()

offset = a.index("\xE8\x00\xF9\xFF\xFF")
noalarm = a[:offset]+"\x90"*5+a[offset+5:]

offset=a.index("\xE8\x39\xFB\xFF\xFF")
nopriv = noalarm[:offset]+"\x90"*5+noalarm[offset+5:]

open("tutorial_",'w').write(nopriv)
