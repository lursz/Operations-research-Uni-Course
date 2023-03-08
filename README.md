# Operations-research-Uni-Class
Set of projects required to pass the class.

```
├── lab-01-augmented-form
│   ├── GRADE.md
│   ├── README.md
│   ├── assignment.pdf
│   ├── assignment.py
│   ├── conftest.py
│   ├── example.py
│   ├── requirements.txt
│   ├── saport
│   │   └── simplex
│   │       ├── expressions
│   │       │   ├── atom.py
│   │       │   ├── constraint.py
│   │       │   ├── expression.py
│   │       │   └── objective.py
│   │       ├── model.py
│   │       ├── solution.py
│   │       ├── solver.py
│   │       └── tableaux.py
│   ├── test_screenshot.png
│   └── tests
│       ├── cases.py
│       └── test_augmented_form.py
├── lab-02-simplex
│   ├── GRADE.md
│   ├── HELP.md
│   ├── README.md
│   ├── example.py
│   ├── example_01_solvable.py
│   ├── example_02_solvable.py
│   ├── example_03_unbounded.py
│   ├── requirements.txt
│   ├── saport
│   │   └── simplex
│   │       ├── exceptions.py
│   │       ├── expressions
│   │       │   ├── constraint.py
│   │       │   ├── expression.py
│   │       │   └── objective.py
│   │       ├── model.py
│   │       ├── solution.py
│   │       ├── solver.py
│   │       └── tableaux.py
│   └── test.py
├── lab-03-two-phase-simplex
│   ├── GRADE.md
│   ├── README.md
│   ├── conftest.py
│   ├── example.py
│   ├── example_01_solvable.py
│   ├── example_02_solvable.py
│   ├── example_03_unbounded.py
│   ├── example_04_solvable_artificial_vars.py
│   ├── example_05_infeasible.py
│   ├── requirements.txt
│   ├── saport
│   │   └── simplex
│   │       ├── exceptions.py
│   │       ├── expressions
│   │       │   ├── constraint.py
│   │       │   ├── expression.py
│   │       │   └── objective.py
│   │       ├── model.py
│   │       ├── solution.py
│   │       ├── solver.py
│   │       └── tableaux.py
│   └── tests
│       └── test_two_phase_simplex_offline.py
├── lab-04-assignment-problem
│   ├── GRADE.htm
│   ├── GRADE.md
│   ├── README.md
│   ├── assignment_tests
│   │   ├── max_04_03_22.txt
│   │   ├── max_04_41.txt
│   │   ├── max_04_44.txt
│   │   ├── min_03_04_12.txt
│   │   ├── min_03_12.txt
│   │   ├── min_03_15.txt
│   │   ├── min_04_03_11.txt
│   │   ├── min_04_03_14.txt
│   │   ├── min_04_20.txt
│   │   └── min_05_124.txt
│   ├── moje_testy.py
│   ├── requirements.txt
│   ├── saport
│   │   ├── assignment
│   │   │   ├── hungarian_solver.py
│   │   │   ├── model.py
│   │   │   └── simplex_solver.py
│   │   └── simplex
│   │       ├── exceptions.py
│   │       ├── expressions
│   │       │   ├── constraint.py
│   │       │   ├── expression.py
│   │       │   └── objective.py
│   │       ├── model.py
│   │       ├── solution.py
│   │       ├── solver.py
│   │       └── tableaux.py
│   └── test.py
├── lab-05-critical-path
│   ├── GRADE.md
│   ├── README.md
│   ├── conftest.py
│   ├── example_input
│   │   ├── project_01.txt
│   │   ├── project_02.txt
│   │   └── project_03.txt
│   ├── functional_test.py
│   ├── requirements.txt
│   ├── saport
│   │   ├── critical_path
│   │   │   ├── model.py
│   │   │   ├── project_network.py
│   │   │   ├── solution.py
│   │   │   └── solvers
│   │   │       ├── cpm_solver.py
│   │   │       ├── networkx_solver.py
│   │   │       ├── simplex_solver_max.py
│   │   │       └── simplex_solver_min.py
│   │   └── simplex
│   │       ├── exceptions.py
│   │       ├── expressions
│   │       │   ├── constraint.py
│   │       │   ├── expression.py
│   │       │   └── objective.py
│   │       ├── model.py
│   │       ├── solution.py
│   │       ├── solver.py
│   │       └── tableaux.py
│   └── tests
│       └── test_critical_path_offline.py
├── lab-06-knapsack-problem
│   ├── GRADE.md
│   ├── README.md
│   ├── benchmark.py
│   ├── conftest.py
│   ├── knapsack_benchmark.py
│   ├── knapsack_problems
│   │   ├── ks_100_0
│   │   ├── ks_19_0
│   │   ├── ks_200_0
│   │   ├── ks_30_0
│   │   ├── ks_40_0
│   │   ├── ks_45_0
│   │   ├── ks_4_0
│   │   ├── ks_500_0
│   │   ├── ks_50_0
│   │   ├── ks_50_1
│   │   ├── ks_60_0
│   │   ├── ks_lecture_dp_1
│   │   └── ks_lecture_dp_2
│   ├── requirements.txt
│   ├── saport
│   │   ├── __init__.py
│   │   └── knapsack
│   │       ├── __init__.py
│   │       ├── model.py
│   │       ├── solver.py
│   │       ├── solverfactory.py
│   │       └── solvers
│   │           ├── bnb_dfs.py
│   │           ├── dfs.py
│   │           ├── dynamic.py
│   │           └── greedy.py
│   └── tests
│       ├── test_bnb_dfs.py
│       ├── test_dynamic.py
│       └── test_greedy.py
└── lab-07-integer-programming
    ├── GRADE.md
    ├── README.md
    ├── benchmark.py
    ├── conftest.py
    ├── knapsack_benchmark.py
    ├── knapsack_problems
    │   ├── ks_19_0
    │   ├── ks_4_0
    │   ├── ks_lecture_dp_1
    │   └── ks_lecture_dp_2
    ├── requirements.txt
    ├── saport
    │   ├── __init__.py
    │   ├── integer
    │   │   ├── model.py
    │   │   ├── solution.py
    │   │   ├── solver.py
    │   │   └── solvers
    │   │       ├── implicit_enumeration.py
    │   │       └── linear_relaxation.py
    │   ├── knapsack
    │   │   ├── __init__.py
    │   │   ├── model.py
    │   │   ├── solver.py
    │   │   ├── solverfactory.py
    │   │   └── solvers
    │   │       ├── bnb_dfs.py
    │   │       ├── dfs.py
    │   │       ├── dynamic.py
    │   │       ├── greedy.py
    │   │       ├── integer_implicit_enumeration.py
    │   │       └── integer_linear_relaxation.py
    │   └── simplex
    │       ├── exceptions.py
    │       ├── expressions
    │       │   ├── constraint.py
    │       │   ├── expression.py
    │       │   └── objective.py
    │       ├── model.py
    │       ├── solution.py
    │       ├── solver.py
    │       └── tableaux.py
    └── tests
        ├── knapsack_problems
        │   ├── ks_4_0
        │   ├── ks_lecture_dp_1
        │   └── ks_lecture_dp_2
        └── test_offline.py
```
