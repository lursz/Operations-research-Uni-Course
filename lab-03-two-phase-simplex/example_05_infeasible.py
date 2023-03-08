import logging
from saport.simplex.model import Model 

from saport.simplex.model import Model

def create_model() -> Model:
    model = Model("example_05_infeasible")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")
    x4 = model.create_variable("x4")

    model.add_constraint(x1 + x2 <= 9)
    model.add_constraint(3*x1 + x2 <= 18)
    model.add_constraint(x1 <= 7)
    model.add_constraint(x2 + x3 + x4 * 5 <= 600)
    model.add_constraint(x1+x2+x3+x4 == 200000)

    model.maximize(3 * x1 + 2 * x2 - x3 - x4)

    #TODO:
    # fill missing test based on the example_03_unbounded.py
    # to make the test a bit more interesting:
    # * make sure model is infeasible
    return model

def run():
    model = create_model()
    #TODO:
    # add a test "assert something" based on the example_03_unbounded.py
    # TIP: you may use other solvers (e.g. https://online-optimizer.appspot.com)
    #      to find the correct solution
    
    solution = model.solve()

    logging.info(solution)

    assert (not solution.is_feasible), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
