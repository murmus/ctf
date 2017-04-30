import copy
 
class Puzzle:
    """
    Class to represent a peg board puzzle, like the triangle peg puzzles
    at Cracker Barrel.
    
    The board attribute stores the current state of the board such that
    a tuple (x, y) representing a position on the board can be accessed
    at board[y][x]. All position tuples are shown in the diagram below:
    
    0,4
    0,3  1,3
    0,2  1,2  2,2
    0,1  1,1  2,1  3,1
    0,0  1,0  2,0  3,0  4,0
    
    As such, (0, 0), (0, 4), and (4, 0) are the three corners of the
    triangle. Captures can happen in six directions:
    
    1. (x, y) to (x+2, y), removing (x+1, y)
    2. (x, y) to (x-2, y), removing (x-1, y)
    3. (x, y) to (x, y+2), removing (x, y+1)
    4. (x, y) to (x, y-2), removing (x, y-1)
    5. (x, y) to (x+2, y-2), removing (x+1, y-1)
    6. (x, y) to (x-2, y+2), removing (x-1, y+1)
    """
    
    def __init__(self, x=0, y=0):
        """Initialize a new puzzle board with one empty peg"""
        
        # build new board attribute to store state of board
        # and set all values to True (has a peg)
        self.board = []
        for row in range(5):
            self.board.append([])
            for col in range(5-row):
                self.board[row].append(True)
        
        # total number of pegs starts at 15
        self.pegs_remaining = 15
        
        # store and remove the starting empty peg
        self.start_peg = (x, y)
        self._remove(x, y)
                
        # create an empty history object to record all moves made
        self.history = []
	print "BOARD BUILT"
    
    def __str__(self):
        """Visualize the board for pretty printing"""
        
        str = ""
        for row in reversed(self.board):
            for pad in range(5 - len(row)):
                str += " "
            for peg in row:
                if peg:
                    str += " *"
                else:
                    str += " ."
            str += "\n"
        return str[:-1]
    
    def __contains__(self, peg):
        """Check if the X and Y coordinates supplied are valid"""
        
        # get x and y values
        x = peg[0]
        y = peg[1]
        
        # negative coordinates are not valid
        if x < 0 or y < 0:
            raise self.PegError("There is no hole at %s,%s" % (x,y))
        
        # do the coordinates exist in the board attribute?
        try:
            p = self.board[y][x]
        except:
            raise self.PegError("There is no hole at %s,%s" % (x,y))
        
        # all good
        return p
    
    def show_moves(self):
        """Visualize the history of all puzzle moves to this point"""

        # create new blank puzzle to show moves with
        p = Puzzle(self.start_peg[0], self.start_peg[1])

	print self.history
        # start building output string by showing starting position
        s = str(p)

        # iterate over each move and ouput the board state
        for move in self.history:
            p.move(move)
            s += "\n\n" + str(p)

        # return the output string
        return s + "\n\nSolved in %s moves." % len(self.history)

    def _remove(self, x, y):
        """Remove the peg at the specified coordinates"""
        
        # sanity check: is there a peg at these coordinates?
        if not (x,y) in self:
            raise self.PegError("There is no peg to remove at %s,%s" % (x,y))
        
        # remove the peg
        self.board[y][x] = False
        self.pegs_remaining -= 1
    
    def _add(self, x, y):
        """Add a peg at the specified coordinates"""
        
        # sanity check: is there already a peg at these coordinates?
        if (x,y) in self:
            raise self.PegError("There is already a peg at %s,%s" % (x,y))
        
        # add the peg
        self.board[y][x] = True
        self.pegs_remaining += 1
    
    def move(self, move):
        """Move a peg and remove the jumped peg"""
        
        # get move values
        x = move.x
        y = move.y
        d = move.direction
        
        # always start by removing the peg we're moving
        self._remove(x, y)
        
        # move forward
        if d == 1:
            self._remove(x + 1, y)
            self._add(x + 2, y)

        # move back
        elif d == 2:
            self._remove(x - 1, y)
            self._add(x - 2, y)
        
        # move up
        elif d == 3:
            self._remove(x, y + 1)
            self._add(x, y + 2)

        # move down
        elif d == 4:
            self._remove(x, y - 1)
            self._add(x, y - 2)
        
        # move down and forward
        elif d == 5:
            self._remove(x + 1, y - 1)
            self._add(x + 2, y - 2)

        # move up and back
        elif d == 6:
            self._remove(x - 1, y + 1)
            self._add(x - 2, y + 2)
        
        # add the move we just made to this board's history
        self.history.append(move)
    
    def solve(self):
        """Find all possible solutions from the current board configuration"""
        
        # iterate over all peg holes on board
        for y,row in enumerate(self.board):
            for x,peg in enumerate(row):
                
                # iterate over all the possible move directions
                for direction in range(1, 7):
                    
                    # make a copy of the board to test the move on
                    branch = copy.deepcopy(self)
                    
                    # try the move
                    try:
                        branch.move(self.Move(x, y, direction))
                        
                        # now that we've moved, is the puzzle solved?
                        if branch.pegs_remaining == 1:
                            return branch
                        
                        # if not, try to solve the puzzle from this new state
                        else:
                            return branch.solve()
                    
                    # the move wasn't valid, so lets move on
                    except:
                        continue
        
        # no possible moves from this position, and puzzle is not solved
        raise self.DeadEnd()
            
                
    class Move:
        """An object to store a single peg move"""
        
        def __init__(self, x, y, direction):
            self.x = x
            self.y = y
            self.direction = direction
                        
    
    class PegError(Exception):
        """Exception for when unable to add/remove peg"""


    class DeadEnd(Exception):
        """Exception for when we've run out of possible moves and the puzzle is not solved"""

if __name__ == "__main__":
	# set up a new puzzle
	p = Puzzle(2,0)

	# solve the puzzle
	print "Looking for solution..."
	try:
	    solution = p.solve()
	    print "\n" + solution.show_moves()

	# show message if no solution was found
	except Puzzle.DeadEnd:
		print "No possible solution"
