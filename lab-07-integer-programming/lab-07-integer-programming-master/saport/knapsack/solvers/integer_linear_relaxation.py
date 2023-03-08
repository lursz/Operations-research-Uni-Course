from saport.knapsack.solver import Solver
from saport.knapsack.model import Problem, Solution, Item
from typing import List
from saport.integer.model import Model
from saport.integer.solvers.linear_relaxation import LinearRelaxationSolver
from saport.simplex.expressions.expression import Expression


class IntegerLinearRelaxationSolver(Solver):
    """
    An Integer Programming solver for the knapsack problems

    Methods:
    --------
    create_model() -> Model:
        creates and returns an integer programming model based on the self.problem
    """
    def create_model(self) -> Model:
        m = Model('knapsack')
        # TODO:
        # - variables: whether the item gets taken
        # - constraints: weights
        # - objective: values
        funkcja_celu, ograniczenie_wagi = Expression(), Expression()
        for i in range(len(self.problem.items)):
            v = m.create_variable("x_{}".format(i))
            funkcja_celu += self.problem.items[i].value * m.variables[i]
            ograniczenie_wagi += self.problem.items[i].weight * m.variables[i]
            m.add_constraint(v <= 1)
        m.add_constraint(ograniczenie_wagi <= self.problem.capacity)
        m.maximize(funkcja_celu)
        return m

    def solve(self) -> Solution:
        m = self.create_model()
        solver = LinearRelaxationSolver()
        integer_solution = solver.solve(m, self.timelimit)
        items = [item for (i, item) in enumerate(self.problem.items) if integer_solution.value(m.variables[i]) > 0]
        solution = Solution.from_items(items, not solver.interrupted)
        return solution