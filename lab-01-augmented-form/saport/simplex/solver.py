from __future__ import annotations
from statistics import mode
from typing import Dict, List

from copy import deepcopy
from . import model as ssmod 
from .expressions import constraint as ssecon
from .expressions import expression as sseexp
from .expressions import objective as sseobj
from . import solution as sssol 
from . import tableaux as sstab
import numpy as np 

class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Tableaux:
            solves the given model and return the first solution
    """
    def solve(self, model: ssmod.Model) -> sssol.Solution:
        augmented_model = self._augment_model(model)
        tableaux = self._basic_initial_tableaux(augmented_model)
        solution = self._extract_solution(tableaux, model)
        return solution
        
    def _augment_model(self, original_model: ssmod.Model) -> ssmod.Model:
        """
            _augment_model(model: Model) -> Model:
                returns an augmented version of the given model 
        """
        # We don't want to modify the original model
        model = deepcopy(original_model)
        # Wa want to have simplified expressions 
        # (each variable) should occur only once in every expression
        model.simplify()

        # TODO:
        # 1. the augmented model is always a maximizing model
        # - if the objective is minimizing, we have to "invert" it
        #   tip. Objective class has an "invert" method just for this purpose
        # 2. all the bounds in the augmented model have to be positive
        # - every model with a negative bound has to be "inverted"
        #   tip. Constraint class has an "invert" method just for this purpose
        # 3. add slack/surplus variables
        # - every GE constraint needs a new surplus variable, that should be subtracted to its expression
        # - every LE constraint needs a new slack variable, that should be added to its expression
        # tip. '-' and '+' operators are overloaded for the expression type, so you can literally add/subtract variables
        # - all constraints in the augmented model should be of type EQ
        
        if model.objective.type == sseobj.ObjectiveType.MIN:
            model.objective.invert()
        
        for i, constraint_instance in enumerate(model.constraints):
            if constraint_instance.bound < 0:
                constraint_instance.invert()
            if constraint_instance.type == ssecon.ConstraintType.GE:
                constraint_instance.expression -= model.create_variable("s" + str(i))
            elif constraint_instance.type == ssecon.ConstraintType.LE:
                constraint_instance.expression += model.create_variable("s" + str(i))
            constraint_instance.type = ssecon.ConstraintType.EQ

        return model  

    def _basic_initial_tableaux(self, model: ssmod.Model) -> sstab.Tableaux:
        # TODO:
        # replace the 'None' below with a numpy array, where
        # 1) first row consists of the inverted coefficients of the objective expression 
        #    plus 0.0 in the last column
        # 2) every other row consists of the coefficitients in the corresponding constraints, 
        #    don't forget to put the constraint bound in the last column
        # tips.
        # - to invert coefficients in the expression, one can multiply it by "-1"
        # - to get coefficients one can use the coefficients method in the expression object
         
        table = np.zeros((len(model.constraints) + 1, len(model.variables) + 1))

        for i, coeff in enumerate(model.objective.expression.coefficients(model)):
            table[0][i] = -coeff
        
        for i in range(len(model.constraints)):
            for j, coeff in enumerate(model.constraints[i].expression.coefficients(model)):
                table[i + 1][j] = coeff
            table[i + 1][-1] = model.constraints[i].bound

        return sstab.Tableaux(model, table)

    def _extract_solution(self, tableaux: sstab.Tableaux, model: ssmod.Model) -> sssol.Solution:
        return sssol.Solution(model, tableaux)