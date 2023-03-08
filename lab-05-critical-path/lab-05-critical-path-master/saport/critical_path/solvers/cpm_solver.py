from curses.ascii import TAB
import networkx as nx
from ..model import Project
from ..project_network import ProjectState, ProjectNetwork
from typing import List, Dict
from ..solution import FullSolution

import copy

class Solver:
    '''
    A "critical path method" solver for the given project.

        Attributes:
    ----------
    project_network: ProjectNetwork
        a project network related to the given project

    Methods:
    --------
    __init__(problem: Project):
        create a solver for the given project
    solve -> FullSolution:
        solves the problem and returns the full solution
    forward_propagation() -> Dict[ProjectState,int]:
        calculates the earliest times the given events (project states) can occur
        returns a dictionary mapping network nodes to the timestamps
    backward_propagation(earliest_times: Dict[ProjectState, int]) -> Dict[ProjectState,int]:
        calculates the latest times the given events (project states) can occur
        uses earliest times to start the computation
        returns a dictionary mapping network nodes to the timestamps
    calculate_slacks(earliest_times: Dict[ProjectState, int], latest_times: Dict[ProjectState,int]) -> Dict[str, int]:
        calculates slacks for every task in the project
        uses earliest times and latest time of the events in the computations
        returns a dictionary mapping tasks names to their slacks
    create_critical_paths(slacks: Dict[str,int]) -> List[List[str]]:
        finds all the critical paths in the project based on the tasks' slacks
        returns list containing paths, every path is a list of tasks names put in the order they occur in the critical path 
    '''
    def __init__(self, problem: Project):
        self.project_network = ProjectNetwork(problem)

    def solve(self) -> FullSolution:
        earliest_times = self.forward_propagation()
        latest_times = self.backward_propagation(earliest_times)
        task_slacks = self.calculate_slacks(earliest_times, latest_times)
        critical_paths = self.create_critical_paths(task_slacks)
        # TODO:
        # set duration of the project based on the gathered data
        duration = earliest_times[self.project_network.goal_node]
        return FullSolution(duration, critical_paths, task_slacks)

    def forward_propagation(self) -> Dict[ProjectState, int]:
        # TODO:
        # earliest time of the project start node is always 0
        # every other event can occur as soon as all its predecessors plus duration of the tasks leading to the state
        #
        # earliest_times[state] = e
        top_it = nx.topological_sort(self.project_network.network)

        earliest_times = {self.project_network.start_node: 0}

        for w in top_it:
            tab = list(self.project_network.predecessors(w))
            if not tab:
                earliest_times[w] = 0
                continue
            earliest_times[w] = max(earliest_times[v] + self.project_network.arc_duration(v, w) for v in tab)

        return earliest_times

    def backward_propagation(self, earliest_times: Dict[ProjectState, int]) -> Dict[ProjectState, int]:
        # TODO:
        # latest time of the project goal node always equals earliest time of the same node
        # every other event occur has to occur before its successors latest time
        latest_times = {self.project_network.goal_node: earliest_times[self.project_network.goal_node]}

        top_it = reversed(list(nx.topological_sort(self.project_network.network)))

        for w in top_it:
            tab = list(self.project_network.successors(w))
            if not tab:
                latest_times[w] = earliest_times[w]
                continue
            latest_times[w] = min(latest_times[v] - self.project_network.arc_duration(w, v) for v in tab)

        return latest_times

    def calculate_slacks(self, 
                         earliest_times: Dict[ProjectState, int], 
                         latest_times: Dict[ProjectState, int]) -> Dict[str, int]:
        # TODO:
        # slack of the task equals "the latest time of its end" minus "earliest time of its start" minus its duration
        # tip: remember to ignore dummy tasks (task.is_dummy could be helpful)
        slacks = {}

        for v, u, zadanie  in self.project_network.edges():
            if zadanie.is_dummy:
                continue
            slacks[zadanie.name] = latest_times[u] - earliest_times[v] - zadanie.duration

        return slacks

    def create_critical_paths(self, slacks: Dict[str, int]) -> List[List[str]]:
        # TODO:
        # critical path start connects start node to the goal node
        # and uses only critical tasks (critical task has slack equal 0)
        # 1. create copy of the project network
        # 2. remove all the not critical tasks from the copy
        # 3. find all the paths from the start node to the goal node
        # 4. translate paths (list of nodes) to list of tasks connecting the nodes
        #
        # tip 2. use method "remove_edge(<start>, <end>" directly on the graph object 
        #        (e.g. self.project_network.network or rather its copy)
        # tip 3. nx.all_simple_paths method finds all the paths in the graph
        # tip 4. if "L" is a list "[1,2,3,4]", zip(L, L[1:]) will return [(1,2),(2,3),(3,4)]

        kopia = copy.deepcopy(self.project_network)

        for v, u, zadanie in kopia.edges():
            if not zadanie.is_dummy and slacks[zadanie.name] != 0:
                kopia.network.remove_edge(v, u)

        krawedzie = {(n[0].index, n[1].index): n[2].name for n in kopia.edges()}
        
        sciezki = list(nx.all_simple_paths(kopia.network, self.project_network.start_node, self.project_network.goal_node))

        critical_paths = [[krawedzie[(sciezka[i].index, sciezka[i + 1].index)] for i in range(len(sciezka) - 1) if krawedzie[(sciezka[i].index, sciezka[i + 1].index)] != "*"] for sciezka in sciezki]

        return critical_paths
