from saport.simplex.model import Model
from saport.simplex.expressions.expression import Expression

#TODO:
# Model assignments from assignment.pdf
# tip 1. you may use an external solver to check if your models reach correct optima
# tip 2. external solver available on-line: https://online-optimizer.appspot.com/?model=builtin:default.mod 

def assignment_1():
    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    # tip. value at optimum: 80.0
    
    model = Model("Assignment 1")
    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    expr1 = x1 + x2 + x3
    expr2 = x1 + 2*x2 + x3
    expr3 = 2*x2 + x3
    expr_objective =  2*x1 + x2 + 3*x3

    model.add_constraint(expr1 <= 30)
    model.add_constraint(expr2 >= 10)
    model.add_constraint(expr3 <= 20)
    
    model.maximize(expr_objective)

    return model

def assignment_2():
    model = Model("Assignment 2")

    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    # tip. value at optimum: 10800.0

    P1 = model.create_variable("P1")
    P2 = model.create_variable("P2")
    P3 = model.create_variable("P3")
    P4 = model.create_variable("P4")

    expr1 = 0.8 * P1 + 2.4 * P2 + 0.9 * P3 + 0.4 * P4
    expr2 = 0.6 * P1 + 0.6 * P2 + 0.3 * P3 + 0.3 * P4
    expr_objective = 9.6 * P1 + 14.4 * P2 + 10.8 * P3 + 7.2 * P4

    model.add_constraint(expr1 >= 1200)
    model.add_constraint(expr2 >= 600)

    model.minimize(expr_objective)

    return model

def assignment_3():
    model = Model("Assignment 3")

    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    # tip. value at optimum: 0.0

    x1 = model.create_variable("steki")
    x2 = model.create_variable("ziemniaki")
  
    expr1 = 5*x1 + 15 * x2
    expr2 = 20 * x1 + 5 * x2
    expr3 = 15 * x1 + 2 * x2
    expr_objective =  8 *x1 + 4* x2 

    model.add_constraint(expr1 >= 50)
    model.add_constraint(expr2 >= 40)
    model.add_constraint(expr3 <= 60)
    
    model.minimize(expr_objective)
 
    return model

def assignment_4():
    model = Model("Assignment 4")

    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    # tip. value at optimum: 4000.0

    x1 = model.create_variable("ulozenie1")
    x2 = model.create_variable("ulozenie2")
    x3 = model.create_variable("ulozenie3")
    x4 = model.create_variable("ulozenie4")
    x5 = model.create_variable("ulozenie5")

    expr_iloscL = x1 + x5
    expr_iloscM = x1 + 2 * x2 + x3
    expr_iloscS = x2 + 3 * x3 + 5 * x4 + 2 * x5
    expr_objective =  20 * x1 + 15 * x2 + 20 * x3 + 25 * x4 + 25 * x5

    model.add_constraint(expr_iloscL >= 150)
    model.add_constraint(expr_iloscM >= 200)
    model.add_constraint(expr_iloscS >= 150)
    
    model.minimize(expr_objective)
 
    return model
