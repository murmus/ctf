from pwn import *

s = remote("quizz.teaser.insomnihack.ch",1031)

s.recvuntil("~~~\n")
s.recvuntil("~~~\n")
s.recvuntil("~~ ")

lookup = {
	'What is the birth year of Paul Kocher ?\n': "1973",
	'What is the birth year of Ralph Merkle ?\n':"1952",
	'What is the birth year of Arjen K. Lenstra ?\n':"1956",
	'What is the birth year of Martin Hellman ?\n':"1945",
	'What is the birth year of Ronald Cramer ?\n':"1968",
	'What is the birth year of Ross Anderson ?\n':"1956",
	'What is the birth year of Moni Naor ?\n':"1961",
	'What is the birth year of Jacques Stern ?\n':"1949",
	'What is the birth year of Tatsuaki Okamoto ?\n':"1952",
	'What is the birth year of Yehuda Lindell ?\n':"1971",
	'What is the birth year of Xuejia Lai ?\n':"1954",
	'What is the birth year of David Naccache ?\n':"1967",
	'What is the birth year of Douglas Stinson ?\n':"1956",
	'What is the birth year of Eli Biham ?\n':"1960",
	'What is the birth year of Dan Boneh ?\n':"1969",
	'What is the birth year of Kaisa Nyberg ?\n':"1948",
	'What is the birth year of Donald Davies ?\n':"1924",
	'What is the birth year of Daniel J. Bernstein ?\n':"1971",
	'What is the birth year of Phil Rogaway ?\n':"1962",
	'What is the birth year of Alex Biryukov ?\n':"1969",
	'What is the birth year of Jim Massey ?\n':"1934",
	'What is the birth year of Whitfield Diffie ?\n':"1944",
	'What is the birth year of Paulo Barreto ?\n':"1965",
	'What is the birth year of Antoine Joux ?\n':"1967",
	'What is the birth year of Niels Ferguson ?\n':"1965",
	'What is the birth year of Horst Feistel ?\n':"1915",
	'What is the birth year of Serge Vaudenay ?\n':"1968",
	'What is the birth year of Lars Knudsen ?\n':"1962",
	'What is the birth year of Michael O. Rabin ?\n':"1931",
	'What is the birth year of Victor S. Miller ?\n':"1947",
	'What is the birth year of Daniel Bleichenbacher ?\n':"1964",
	'What is the birth year of Claus-Peter Schnorr ?\n':"1943",
	'What is the birth year of Yvo Desmedt ?\n':"1956",
	}

buf = '\n'
while 1:
	while buf == '\n':
		buf = s.recvline()
	print repr(buf)
	if buf in lookup.keys():
		print "FOUND"
		s.sendline(lookup[buf])
		s.recvuntil("~~ ")
		buf = s.recvline()
	else:
		s.interactive()
		break
	
