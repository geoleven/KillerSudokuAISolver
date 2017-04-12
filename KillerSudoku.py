import itertools
import re
from csp import *


class KilSud:
    cells = []
    cage_map = []
    cage_sizes = []

    def __init__(self, my_cells, my_cage_map,  my_cage_sizes):
        self.cells = my_cells
        self.cage_map = my_cage_map
        self.cage_sizes = my_cage_sizes


def different_values_constraint(A, a, B, b):
    "A constraint saying two neighboring variables must differ in value."
    return a != b


def flatten(seqs):
    return sum(seqs, [])


def print_grid(grid):
    for counter in range(0, 81):
        print(grid[counter]),
        if counter % 3 == 2:
            print "  ",
        if counter % 9 == 8:
            print "\n",
        if counter % 27 == 26:
            print "\n",
    print "\n\n"

#easy1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
#easy1 = KilSud('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..',
#easy1 = KilSud('.................................................................................',
easy1 = KilSud([2, 0, 5,   6, 0, 0,   3, 0, 0,
                0, 0, 0,   0, 5, 2,   0, 7, 0,
                0, 9, 0,   3, 8, 1,   6, 0, 0,

                0, 0, 6,   2, 0, 0,   0, 3, 0,
                1, 4, 2,   0, 9, 0,   0, 6, 0,
                0, 0, 3,   0, 1, 0,   4, 0, 0,

                0, 0, 1,   7, 0, 0,   0, 0, 0,
                6, 0, 0,   4, 2, 8,   0, 0, 0,
                0, 0, 0,   0, 0, 0,   0, 0, 9],

               [0,  0,  1,    1,  1,  2,    3,  4,  5,
                6,  6,  7,    7,  2,  2,    3,  4,  5,
                6,  6,  8,    8,  2,  9,    10, 10, 5,

                11, 12, 12,   8,  13,  9,   10, 14, 5,
                11, 15, 15,   16, 13,  9,   14, 14, 17,
                18, 15, 19,   16, 13, 20,   21, 21, 17,

                18, 19, 19,   16, 22, 20,   20, 23, 23,
                18, 24, 25,   22, 22, 26,   26, 23, 23,
                18, 24, 25,   22, 27, 27,   27, 28, 28],
               [3, 15, 22, 4, 16, 15, 25, 17, 9, 8, 20, 6, 14, 17, 17, 13, 20, 12, 27, 6, 20, 6, 10, 14, 8, 16, 15, 13,
                17])
#harder1 = KilSud('4173698.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......',
#                 '.................................................................................')

print_grid(easy1.cells)

class KillerSudoku(CSP):
    """A Sudoku problem.
    The box grid is a 3x3 array of boxes, each a 3x3 array of cells.
    Each cell holds a digit in 1..9. In each box, all digits are
    different; the same for each row and column as a 9x9 grid.
    >>> e = KillerSudoku(easy1)
    >>> e.display(e.infer_assignment())
    . . 3 | . 2 . | 6 . .
    9 . . | 3 . 5 | . . 1
    . . 1 | 8 . 6 | 4 . .
    ------+-------+------
    . . 8 | 1 . 2 | 9 . .
    7 . . | . . . | . . 8
    . . 6 | 7 . 8 | 2 . .
    ------+-------+------
    . . 2 | 6 . 9 | 5 . .
    8 . . | 2 . 3 | . . 9
    . . 5 | . 1 . | 3 . .
    >>> AC3(e); e.display(e.infer_assignment())
    True
    4 8 3 | 9 2 1 | 6 5 7
    9 6 7 | 3 4 5 | 8 2 1
    2 5 1 | 8 7 6 | 4 9 3
    ------+-------+------
    5 4 8 | 1 3 2 | 9 7 6
    7 2 9 | 5 6 4 | 1 3 8
    1 3 6 | 7 9 8 | 2 4 5
    ------+-------+------
    3 7 2 | 6 8 9 | 5 1 4
    8 1 4 | 2 5 3 | 7 6 9
    6 9 5 | 4 1 7 | 3 8 2
    >>> h = KillerSudoku(harder1)
    >>> None != backtracking_search(h, select_unassigned_variable=mrv, inference=forward_checking)
    True
    """
    grid = KilSud
    R3 = range(3)
    Cell = itertools.count().next
    bgrid = [[[[Cell() for x in R3] for y in R3] for bx in R3] for by in R3]
    boxes = flatten([map(flatten, brow) for brow in bgrid])
    rows = flatten([map(flatten, zip(*brow)) for brow in bgrid])
    cols = zip(*rows)

    neighbors = dict([(v, set()) for v in flatten(rows)])
    for unit in map(set, boxes + rows + cols):
        for v in unit:
            neighbors[v].update(unit - set([v]))


    def killer_sudoku_constraints(self, pos_of_a, a, pos_of_b, b):
        temp_sum_a = 0
        temp_sum_b = 0
        # for counter in self.infer_assignment().keys():
        #     print counter,
        # print "\n\n"
        # if self.grid.cage_map[pos_of_a] == self.grid.cage_map[pos_of_b]:
        #     if not different_values_constraint(pos_of_a, a, pos_of_b, b):
        #         return False
        for counter in self.infer_assignment().keys():
            if counter != pos_of_a:
                if (self.grid.cage_map)[counter] == (self.grid.cage_map)[pos_of_a]:
                    # print "pos: ", self.grid.cage_map[A], "size: ", self.grid.cage_sizes[self.grid.cage_map[A]]
                    #print int((self.infer_assignment())[counter])
                    if (self.infer_assignment())[counter] != '.':
                        temp_sum_a += int((self.infer_assignment())[counter])
            if counter != pos_of_b:
                if (self.grid.cage_map)[counter] == (self.grid.cage_map)[pos_of_b]:
                    if (self.infer_assignment())[counter] != '.':
                        temp_sum_b += int((self.infer_assignment())[counter])
        #print temp_sum_a
        if temp_sum_a <= ((self.grid.cage_sizes)[((self.grid.cage_map)[pos_of_a])] + int(a)):
            if temp_sum_b <= ((self.grid.cage_sizes)[((self.grid.cage_map)[pos_of_b])] ):#+ int(b)):
                #return different_values_constraint(A, a, B, b)
                if different_values_constraint(pos_of_a, a, pos_of_b, b):
                    #print "True"
                    #self.display(self.infer_assignment())
                    #print "\n\n"
                    return True
        #     else:
        #         return False
        # else:
        #     return False
        #print "False"
        return False

    def __init__(self, grid):
        """Build a Sudoku problem from a string representing the grid:
        the digits 1-9 denote a filled cell, '.' or '0' an empty one;
        other characters are ignored."""
        self.grid = grid
        #squares = iter(re.findall(r'\d|\.', grid.cells))
        for counter in range(81):
            for counter2 in range(81):
                if counter != counter2:
                    if self.grid.cage_map[counter] == self.grid.cage_map[counter2]:
                        if counter2 not in self.neighbors[counter]:
                            self.neighbors[counter].add(counter2)
        squares = iter(str(x) if x != 0 else '.' for x in grid.cells)
        domains = dict((var, if_(ch in '123456789', [ch], '123456789'))
                       for var, ch in zip(flatten(self.rows), squares))

        for _ in squares:
            raise ValueError("Not a Sudoku grid", grid.cells)  # Too many squares
        print domains, "\n\n\n"
        print self.neighbors
        CSP.__init__(self, None, domains, self.neighbors,
                     self.killer_sudoku_constraints)

    def display(self, assignment):
        def show_box(box):
            return [' '.join(map(show_cell, row)) for row in box]

        def show_cell(cell):
            return str(assignment.get(cell, '.'))

        def abut(lines1, lines2):
            return map(' | '.join, zip(lines1, lines2))
        print '\n------+-------+------\n'.join(
            '\n'.join(reduce(abut, map(show_box, brow))) for brow in self.bgrid)


p = KillerSudoku(easy1)
p.display(p.infer_assignment())
print "\n\n"
#None != backtracking_search(p)
#None != backtracking_search(p, select_unassigned_variable=mrv)
#None != backtracking_search(p, inference=forward_checking)
None != backtracking_search(p, select_unassigned_variable=mrv, inference=forward_checking)
True
#backtracking_search(p, select_unassigned_variable=mrv, inference=forward_checking)
#print_grid(easy1.cells)
p.display(p.infer_assignment())
