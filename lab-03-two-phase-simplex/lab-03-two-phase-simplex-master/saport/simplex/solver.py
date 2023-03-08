from __future__ import annotations
import sys
from typing import Dict, List

from copy import deepcopy
import saport.simplex.model as ssmod 
import saport.simplex.expressions.objective as sseobj
import saport.simplex.expressions.constraint as ssecon
import saport.simplex.expressions.expression as sseexp
import saport.simplex.solution as sssol
import saport.simplex.tableaux as sstab
import numpy as np 

class Solver:
    """
        A class to represent a simplex solver.

        Attributes:
        ______
        _slacks: Dict[Variable, Constraint]:
            contains mapping from slack variables to their corresponding constraints
        _surpluses: Dict[Variable, Constraint]:
            contains mapping from surplus variables to their corresponding constraints
        _artificial: Dict[Variable, Constraint]:
            contains mapping from artificial variables to their corresponding constraints

        Methods
        -------
        solve(model: Model) -> Tableaux:
            solves the given model and return the first solution
    """
    _slacks: Dict[sseexp.Variable, ssecon.Constraint]
    _surpluses: Dict[sseexp.Variable, ssecon.Constraint]
    _artificial: Dict[sseexp.Variable, ssecon.Constraint]

    def solve(self, model: ssmod.Model):
        normal_model = self._augment_model(model)
        if len(self._slacks) < len(normal_model.constraints):
            tableaux, success = self._presolve(normal_model)
            if not success:
                return sssol.Solution.infeasible(model, tableaux, tableaux)
        else:
            tableaux = self._basic_initial_tableaux(normal_model)
        
        initial_tableaux = deepcopy(tableaux)
        if self._optimize(tableaux) == False:
            return sssol.Solution.unbounded(model, initial_tableaux, tableaux)

        assignment = tableaux.extract_assignment()
        return self._create_solution(assignment, model, initial_tableaux, tableaux)

    def _optimize(self, tableaux: sstab.Tableaux):
        while not tableaux.is_optimal():
            pivot_col = tableaux.choose_entering_variable()
            if tableaux.is_unbounded(pivot_col):
                return False
            pivot_row = tableaux.choose_leaving_variable(pivot_col)

            tableaux.pivot(pivot_row, pivot_col)
        return True

    def _presolve(self, model: ssmod.Model):
        """
            _presolve(model: Model) -> Tableaux:
                returns an initial tableaux for the second phase of simplex
        """
        presolve_model = self._create_presolve_model(model)
        tableaux = self._presolve_initial_tableaux(presolve_model)
        
        self._optimize(tableaux)

        if self._artifical_variables_are_positive(tableaux):
            return (tableaux, False)

        tableaux = self._restore_initial_tableaux(tableaux, model)
        return (tableaux, True)

    def _augment_model(self, original_model: ssmod.Model):
        """
            _augment_model(model: Model) -> Model:
                returns an augmented version of the given model 
        """
        model = deepcopy(original_model)
        model.simplify()
        self._change_objective_to_max(model)
        self._change_constraints_bounds_to_nonnegative(model)
        self._slacks = self._add_slack_variables(model)
        self._surpluses = self._add_surplus_variables(model)   
        return model  

    def _create_presolve_model(self, augmented_model: ssmod.Model):
        presolve_model = deepcopy(augmented_model)
        self._artificial = self._add_artificial_variables(presolve_model)
        return presolve_model    

    def _change_objective_to_max(self, model: ssmod.Model):
        if model.objective.type == sseobj.ObjectiveType.MIN:
            model.objective.invert()
            

    def _change_constraints_bounds_to_nonnegative(self, model: ssmod.Model):
        for constraint in model.constraints:
            if constraint.bound < 0:
                constraint.invert()
    
    def _add_slack_variables(self, model: ssmod.Model) -> List[sseexp.Variable]:
        slacks: Dict[sseexp.Variable, ssecon.Constraint] = dict()

        for constraint in model.constraints:
            if constraint.type == ssecon.ConstraintType.LE:
                slack_var = model.create_variable(f"s{constraint.index}")
                slacks[slack_var] = constraint
                constraint.expression = constraint.expression + slack_var
                constraint.type = ssecon.ConstraintType.EQ

        return slacks

    def _add_surplus_variables(self, model: ssmod.Model) -> List[sseexp.Variable]:
        surpluses: Dict[sseexp.Variable, ssecon.Constraint] = dict()

        for constraint in model.constraints:
            if constraint.type == ssecon.ConstraintType.GE:
                surplus_var = model.create_variable(f"s{constraint.index}")
                surpluses[surplus_var] = constraint
                constraint.expression = constraint.expression - surplus_var
                constraint.type = ssecon.ConstraintType.EQ

        return surpluses 

    def _add_artificial_variables(self, model: ssmod.Model):
        artificial_variables: Dict[sseexp.Variable, ssecon.Constraint] = dict()

        indeksy = set([constraint.index for constraint in self._slacks.values()])

        for constraint in model.constraints:
            if constraint.index not in indeksy:
                var = model.create_variable(f"R" + str(constraint.index))
                artificial_variables[var] = constraint
                constraint.expression += var

        #TODO: add artificial variables to the model.
        #      tip 1. you may base your code on the methods: _add_slack_variables/_add_surplus_variable 
        #      tip 2. artificial variables have to be added only to the constraints without slacks
        #             - self._slacks.values() is a list of constraints where the slacks have been added
        #             - to check if a given constraint is in the list, compare its index with their indices
        #               (constraint class has an `index` attribute, you may use, e.g. c1.index == c2.index)
        return artificial_variables

    def _basic_initial_tableaux(self, model: ssmod.Model):
        objective_row = np.array((-1 * model.objective.expression).coefficients(model) + [0.0])
        table = np.array([objective_row] + [c.expression.coefficients(model) + [c.bound] for c in model.constraints])
        return sstab.Tableaux(model, table)

    def _presolve_initial_tableaux(self, model: ssmod.Model):
        # TODO: create an initial tableaux for the artificial variables
        #       - objective row should contain 1.0 for every artificial variable
        #       - then fix the tableaux basis (tip. artificial variables should be basic) using simple transformations; 
        #         like in the pivot: subtract rows / multiply by constant
        #       tip 1. you may look at the _basic_initial_tableaux on how to create a tableaux
        table = self._basic_initial_tableaux(model).table

        table[0] *= 0
        for i in self._artificial:
            table[0, i.index] = 1

        for i in self._artificial:
            table[0] -= table[self._artificial[i].index + 1]

        return sstab.Tableaux(model, table)

    def _artifical_variables_are_positive(self, tableaux: sstab.Tableaux):
        assignment = tableaux.extract_assignment()
        
        for zmienna in self._artificial:
            if assignment[zmienna.index] > 0:
                return True

        # TODO: check whether any artificial variable in the table is positive
        #       tip 1. `self._artificial` contains info about the artificial variables
        #       tip 2. use `tableaux.extract_assignment` or `tableaux.extract_basis`
        #           - `Variable` class has an `index` attribute, e.g. you may use
        #             `assignment[var.index]` to get value of the variable `var` in the assignment 
        return False

    def _restore_initial_tableaux(self, tableaux: sstab.Tableaux, model: ssmod.Model):
        # TODO: remove artificial variables from the tableaux and restore the objective
        #       1. remove corresponding columns from the tableaux (`np.delete` is a little helper here)
        #       2. restore the original objective row
        #       3. similarly to the way we have zeroed the artificial variables in `_presolve_initial_tableaux`,
        #          now we have to transform the tableaux to make the basic variables (basic = being part of the basis) 
        #          in the first phase tableaux also basic in the new tableaux
        indeksy = [var.index for var in self._artificial.keys()]
        new_table = np.delete(tableaux.table, indeksy, 1)

        new_table[0] = np.array((-1 * model.objective.expression).coefficients(model) + [0.0])

        for col in range(len(new_table[0])):
            collumn = new_table[1:, col]
            if collumn.min() == 0.0 and collumn.max() == 1.0:
                # jest bazowa
                new_table[0] -= new_table[0, col] * new_table[collumn.argmax() + 1]

        return sstab.Tableaux(tableaux.model, new_table)

    def _create_solution(self, assignment: List[float], model: ssmod.Model, initial_tableaux: sstab.Tableaux, tableaux: sstab.Tableaux):
        return sssol.Solution.with_assignment(model, assignment, initial_tableaux, tableaux)