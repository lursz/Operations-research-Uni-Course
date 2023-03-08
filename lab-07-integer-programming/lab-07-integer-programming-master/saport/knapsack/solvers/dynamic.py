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
        table = None
        return table

    def extract_solution(self, table: ArrayLike) -> Solution:
        used_items = []
        optimal = table[-1, -1] > 0

        # TODO: extract taken items from the table!

        return Solution.from_items(used_items, optimal)

    def solve(self) -> Tuple[Solution, float]:
        self.interrupted = False
        self.start_timer()

        table = self.create_table()
        solution = self.extract_solution(table) if table is not None else Solution.empty()

        self.stop_timer()
        return solution
