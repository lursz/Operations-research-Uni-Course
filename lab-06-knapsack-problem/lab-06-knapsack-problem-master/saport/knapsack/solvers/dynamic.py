from ..solver import Solver
from ..model import Solution
from numpy.typing import ArrayLike
import numpy as np
from typing import Tuple


class DynamicSolver(Solver):
    """
    A naive dynamic programming solver for the knapsack problem.
    """

    def create_table(self) -> ArrayLike:
        # TODO: fill the table!
        # tip 1. init table using np.zeros function
        # tip 2. remember to handle timeout (refer to the dfs solver for an example)
        #        - just return the current state of the table

        pojemnosc, ile_przedmiotow = self.problem.capacity, len(self.problem.items)
        table = np.zeros((pojemnosc + 1, ile_przedmiotow + 1))

        for i in range(1, ile_przedmiotow + 1):
            for j in range(1, pojemnosc + 1):
                if self.timeout():
                    self.interrupted = True
                    return table
                
                if self.problem.items[i - 1].weight <= j:
                    table[j, i] = max(table[j, i - 1], table[j - self.problem.items[i - 1].weight, i - 1] + self.problem.items[i - 1].value)
                else:
                    table[j, i] = table[j, i - 1]
        
        return table

    def extract_solution(self, table: ArrayLike) -> Solution:
        used_items = []
        optimal = table[-1, -1] > 0

        # TODO: extract taken items from the table!

        ciezar, ile_przedm = table.shape[0] - 1, table.shape[1] - 1

        while ciezar != 0 and ile_przedm != 0:
            if table[ciezar, ile_przedm] == table[ciezar, ile_przedm - 1]:
                ile_przedm -= 1
            else:
                used_items.append(self.problem.items[ile_przedm - 1])
                ciezar -= self.problem.items[ile_przedm - 1].weight
                ile_przedm -= 1

        return Solution.from_items(used_items, optimal)

    def solve(self) -> Tuple[Solution, float]:
        self.interrupted = False
        self.start_timer()

        table = self.create_table()
        solution = self.extract_solution(table) if table is not None else Solution.empty()

        self.stop_timer()
        return solution
