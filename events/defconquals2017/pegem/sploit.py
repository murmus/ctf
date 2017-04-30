from pwn import *

#s = remote("pegem_d144a0fa24a0fc17809d4f56600bc740.quals.shallweplayaga.me",1234)

converter = [['k','g','d','b','a'],['l','h','e','c'],['m','i','f'],['n','j'],['o']]
import test2

f = open("dmp",'w')
def getBoard(board):
	for row in xrange(len(board)):
		line = board[row]
		sl = line.rstrip().lstrip()
		print sl
		if not sl.isupper():
			print "----", sl, row
			pegs = sl.split()
			print pegs
			for col in xrange(len(pegs)):
				if pegs[col].islower():
					break
			break
	return row, col

try:
	s = process("./pegem")

	s.recvuntil("game\n")
	s.recvline()

	for i in xrange(15):
		board = s.recvline()
		board += s.recvline()
		board += s.recvline()
		board += s.recvline()
		board += s.recvline()

		board = board.split("\n")[:-1]
		board = board[::-1]

		row, col = getBoard(board)

		key = open("solns/%d%d" % (row,col)).read()
		count = len(key.split("\n"))
		print key
		print count
		for line in key.split("\n")[:-1]:
			s.sendline(line)
			f.write(line+"\n")
			print line

		for j in xrange(5*count-5):
			s.recvline()
		print repr(s.recvline())
	name = cyclic(0x125)
	s.sendline(name)
	f.write(name)
	f.close()
	s.interactive()
except Exception as e:
	print e
	
	print board
	print row, col
	p = test2.Puzzle(row,col)

	s = p.solve()

	f = open("solns/%d%d" % (row,col), 'w')
	for move in s.history:
		y = move.x
		x = move.y
		d = move.direction

		if d == 1:
			nx = x
			ny = y+2
		if d == 2:
			nx = x
			ny = y-2
		if d == 3:
			nx = x+2
			ny = y
		if d == 4:
			nx = x-2
			ny = y
		if d == 5:
			nx = x-2
			ny = y+2
		if d == 6:
			nx = x+2
			ny = y-2

		l = converter[x][y].upper()+converter[nx][ny]
		print x, y, d, l
		f.write("%s\n" % l)
	f.close()
