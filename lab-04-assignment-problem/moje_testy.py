import stopit
import saport.assignment.model as sam
import saport.assignment.hungarian_solver as sahs
import saport.assignment.simplex_solver as sass
from saport.simplex.exceptions import EmptyModelError
import numpy as np

c1 = np.array([[0, 9, 0, 4], [0, 7, 6, 1], [2, 0, 0, 0], [0, 3, 5, 3]])
a1 = {1: 0, 0: 2, 2: 1}

print(c1)
sahs.Solver.add_zero_by_crossing_out(None, c1, a1)
print(c1)

c2 = np.array([[0, 5, 4, 1], [1, 2, 0, 3], [3, 5, 0, 5], [0, 0, 0, 0]])
a2 = {0: 0, 1: 2, 3: 1}

print(c2)
sahs.Solver.add_zero_by_crossing_out(None, c2, a2)
print(c2)
