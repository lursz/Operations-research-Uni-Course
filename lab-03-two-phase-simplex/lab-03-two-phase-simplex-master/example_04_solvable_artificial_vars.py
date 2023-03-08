import logging
from saport.simplex.model import Model 

from saport.simplex.model import Model

import numpy as np

def create_model() -> Model:
    model = Model("example_04_solvable_artificial")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")
    x4 = model.create_variable("x4")

    model.add_constraint(x1 + x2 <= 9)
    model.add_constraint(3*x1 + x2 <= 18)
    model.add_constraint(x1 <= 7)
    model.add_constraint(x2 <= 6)
    model.add_constraint(x1 + x2 + x3 + x4 == 20)

    model.maximize(3 * x1 + 2 * x2 - x3 - x4)
    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make sure solver has to use some artificial variables
    return model

def run():
    model = create_model()
    #TODO:
    # add a test "assert something" based on the example_01_solvable.py
    # TIP: you may use other solvers (e.g. https://online-optimizer.appspot.com)
    #      to find the correct solution
    try:
        solution = model.solve()
    except:
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)

    assert (np.allclose(solution.assignment(model), [4.5, 4.5, 0.0, 11.0], rtol = 0.000000001)), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
