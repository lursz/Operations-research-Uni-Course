import logging
from saport.simplex.model import Model 

def create_model() -> Model:
    model = Model(__file__)

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(x1 >= 3)
    model.add_constraint(x1 + x2 >= 10)

    model.maximize(x1 + 2 * x2)
    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make the model unbounded!

    return model 

def run():
    model = create_model()
    #TODO:
    # add a test "assert something" based on the example_01_solvable.py
    #
    # TIP: you may use other solvers (e.g. https://online-optimizer.appspot.com)
    #      to find the correct solution
    #logging.info("This test is empty but it shouldn't be, fix it!")
    #raise AssertionError("Test is empty")

    try:
        solution = model.solve()
    except:
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    assert (not solution.is_bounded), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()