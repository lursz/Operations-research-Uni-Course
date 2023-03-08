from ..model import Project
from ..project_network import ProjectNetwork
from ...simplex.model import Model
from ...simplex.expressions.expression import Expression
from ..solution import BasicSolution

import numpy as np

def var_sum(tablica) -> Expression:
    if not tablica:
        return None
    suma = tablica[0]
    for i in range(1, len(tablica)):
        suma += tablica[i]
    return suma

class Solver:
    '''
    Simplex based solver looking for the critical path in the project.
    Uses linear model maximizing length of the path in the project network. 

    Attributes:
    ----------
    project_network: ProjectNetwork
        a project network related to the given project
    model: simplex.model.Model
        a linear model looking for the maximal path in the project network
    Methods:
    --------
    __init__(problem: Project)
        create a solver for the given project
    create_model() -> simplex.model.Model
        builds a linear model of the problem
    solve() -> BasicSolution
        finds the duration of the critical (longest) path in the project network
    '''
    def __init__(self, problem: Project):
        self.project_network = ProjectNetwork(problem)
        self.model = self.create_model()

    def create_model(self) -> Model:
        # TODO:
        # 0) we need as many variables as there is edges in the project network
        # 1) every variable has to be <= 1
        # 2) sum of the variables starting at the initial state has to be equal 1
        # 3) sum of the variables ending at the goal state has to be equal 1
        # 4) for every other node, total flow going trough it has to be equal 0
        #    i.e. sum of incoming arcs minus sum of the outgoing arcs = 0
        # 5) we have to maximize length of the path
        #    (sum of variables weighted by the durations of the corresponding tasks)
        model = Model("critical path (max)")

        wierzcholki = self.project_network.nodes()
        krawedzie = self.project_network.edges()
        variables = {n : model.create_variable("zmienna{}".format(i)) for i, n in enumerate(krawedzie)}

        for krawedz in krawedzie:
            model.add_constraint(Expression(variables[krawedz]) <= 1.0)
        
        model.add_constraint(var_sum([Expression(variables[(self.project_network.start_node, v, self.project_network.arc_task(self.project_network.start_node, v))]) for v in self.project_network.successors(self.project_network.start_node)]) == 1)
        model.add_constraint(var_sum([Expression(variables[(v, self.project_network.goal_node, self.project_network.arc_task(v, self.project_network.goal_node))]) for v in self.project_network.predecessors(self.project_network.goal_node)]) == 1)

        for wierzcholek in wierzcholki:
            if wierzcholek != self.project_network.start_node and wierzcholek != self.project_network.goal_node:
                wchodzace = [(v, wierzcholek, self.project_network.arc_task(v, wierzcholek)) for v in self.project_network.predecessors(wierzcholek)]
                wychodzace = [(wierzcholek, v, self.project_network.arc_task(wierzcholek, v)) for v in self.project_network.successors(wierzcholek)]
                model.add_constraint(var_sum([Expression(variables[krawedz]) for krawedz in wychodzace]) - var_sum([Expression(variables[krawedz]) for krawedz in wchodzace]) == 0)
        
        # tu zrobic objective
        model.maximize(var_sum([Expression(variables[krawedz]) * krawedz[2].duration for krawedz in krawedzie]))

        return model

    def solve(self) -> BasicSolution:
        solution = self.model.solve()
        return BasicSolution(int(solution.objective_value()))