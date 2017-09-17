'''

pseudo code for the encrypt function:

in = sum([byte for byte in input])
out = 0
for i in flaglen:
	t = in ** i
	c = c * t
	out += c

which is then compared against i in the following script, and prints out a different message if it does

'''

i = 457872149190039938449409450797259650244955817397381468272138729997481631896039607738236

out = ""
while i:
	t = i % 2669
	i = i / 2669

	out += chr(t)
	print out
