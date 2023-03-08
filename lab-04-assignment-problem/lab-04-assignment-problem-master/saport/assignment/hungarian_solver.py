import numpy as np
from .model import Assignment, AssignmentProblem, NormalizedAssignmentProblem
from typing import List, Dict, Tuple, Set
from numpy.typing import ArrayLike

import time

class Solver:
    '''
    A hungarian solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    extract_mins(costs: ArrayLike):
        substracts from columns and rows in the matrix to create 0s in the matrix
    find_max_assignment(costs: ArrayLike) -> Dict[int,int]:
        finds the biggest possible assinments given 0s in the cost matrix
        result is a dictionary, where index is a worker index, value is the task index
    add_zero_by_crossing_out(costs: ArrayLike, partial_assignment: Dict[int,int])
        creates another zero(s) in the cost matrix by crossing out lines (rows/cols) with zeros in the cost matrix,
        then substracting/adding the smallest not crossed out value
    create_assignment(raw_assignment: Dict[int, int]) -> Assignment:
        creates an assignment instance based on the given dictionary assignment
    '''
    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        costs = np.array(self.problem.costs)

        while True:
            self.extracts_mins(costs)
            max_assignment = self.find_max_assignment(costs)
            if len(max_assignment) == self.problem.size():
                return self.create_assignment(max_assignment)
            self.add_zero_by_crossing_out(costs, max_assignment)

    def extracts_mins(self, costs: ArrayLike):
        # substract minimal values from each row and column
        for i in range(costs.shape[0]):
            costs[i] -= np.min(costs[i])
        for i in range(costs.shape[1]):
            costs[:, i] -= np.min(costs[:, i])

    def add_zero_by_crossing_out(self, costs: ArrayLike, partial_assignment: Dict[int,int]):
        # TODO: 1) "mark" columns and rows according to the instructions given by teacher
        # 2) cross out marked columns and not marked rows
        # 3) find minimal uncrossed value and subtract it from the cost matrix
        # 4) add the same value to all crossed out columns and rows
        n = costs.shape[0]

        zazn_wiersze, zazn_kol = np.array([False] * n), np.array([False] * n)
        ile_zer_wiersze = np.array([n - np.count_nonzero(costs[i]) for i in range(n)])
        ile_zer_kolumny = np.array([n - np.count_nonzero(costs[:, i]) for i in range(n)])

        for best_worker in partial_assignment:  
            if ile_zer_wiersze[best_worker] >= ile_zer_kolumny[partial_assignment[best_worker]]:
                zazn_wiersze[best_worker] = True
                for i in range(n):
                    if costs[best_worker, i] == 0:
                        ile_zer_kolumny[i] -= 1
            else:
                zazn_kol[partial_assignment[best_worker]] = True
                for i in range(n):
                    if costs[i, partial_assignment[best_worker]] == 0:
                        ile_zer_wiersze[i] -= 1

        indeksy_krzyz_wiersze, indeksy_krzyz_kol = np.array([], dtype = int), np.array([], dtype = int)

        for i in range(n):
            if zazn_wiersze[i]:
                indeksy_krzyz_wiersze = np.append(indeksy_krzyz_wiersze, i)

        for i in range(n):
            if zazn_kol[i]:
                indeksy_krzyz_kol = np.append(indeksy_krzyz_kol, i)
        
        wartosc_min = -1
        for i in range(n):
            for j in range(n):
                if not zazn_wiersze[i] or not zazn_kol[i]:
                    if costs[i, j] == 0:
                        continue
                    if wartosc_min == -1 or wartosc_min > costs[i, j]:
                        wartosc_min = costs[i, j]
                    
        if wartosc_min == -1:
            return

        costs -= wartosc_min

        for i in indeksy_krzyz_wiersze:
            costs[i] += wartosc_min
        for i in indeksy_krzyz_kol:
            costs[:, i] += wartosc_min


    def find_max_assignment(self, costs) -> Dict[int,int]:
        partial_assignment = dict()
        # find the biggest assignment in the cost matrix
        # 1) always try first the row with the least amount of 0s
        # 2) then use column with the least amount of 0s
        # TIP: remember, rows and cols can't repeat in the assignment
        #      partial_assignment[1] = 2 means that the worker with index 1
        #                                has been assigned to task with index 2

        n = costs.shape[0]

        ile_zer_wiersze = np.array([n - np.count_nonzero(costs[i]) for i in range(n)])
        ile_zer_kolumny = np.array([n - np.count_nonzero(costs[:, i]) for i in range(n)])

        uzyte_wiersze = [False] * n
        uzyte_kolumny = [False] * n

        for i in range(n):
            nr_wiersz = -1

            for j in range(n):
                if uzyte_wiersze[j]:
                    continue
                if ile_zer_wiersze[j] != 0 and (nr_wiersz == -1 or ile_zer_wiersze[nr_wiersz] > ile_zer_wiersze[j]):
                    nr_wiersz = j

            if nr_wiersz == -1:
                break

            nr_kol = -1
            for j in range(n):
                if uzyte_kolumny[j]:
                    continue
                if costs[nr_wiersz, j] == 0 and (nr_kol == -1 or ile_zer_kolumny[nr_kol] > ile_zer_kolumny[j]):
                    nr_kol = j
                
            partial_assignment[nr_wiersz] = nr_kol

            # teraz usuwanie tego wiersza i kolumny
            uzyte_wiersze[nr_wiersz] = True
            uzyte_kolumny[nr_kol] = True

            # zmiana ilosci zer, ktore zostaly
            for j in range(n):
                if costs[j, nr_kol] == 0:
                    ile_zer_wiersze[j] -= 1
                if costs[nr_wiersz, j] == 0:
                    ile_zer_kolumny[j] -= 1

        return partial_assignment

    def create_assignment(self, raw_assignment: Dict[int,int]) -> Assignment:
        # create an assignment instance based on the dictionary
        # tips:
        # 1) use self.problem.original_problem.costs to calculate the cost
        # 2) in case the original cost matrix (self.problem.original_problem.costs wasn't square)
        #    and there is more workers than task, you should assign -1 to workers with no task

        n, m = self.problem.original_problem.n_workers(), self.problem.original_problem.n_tasks()

        assignment = [-1] * n
        total_cost = 0

        for i in raw_assignment:
            if i < n and raw_assignment[i] < m:
                assignment[i] = raw_assignment[i]
                total_cost += self.problem.original_problem.costs[i, raw_assignment[i]]

        return Assignment(assignment, total_cost)