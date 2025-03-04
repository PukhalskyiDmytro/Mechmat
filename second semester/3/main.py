from biquadratic_equation import BiquadraticEquation, QuadraticEquation, Equation

if __name__ == "__main__":
    files = ["input01.txt", "input02.txt", "input03.txt"]
    equations = []
    zero_solutions = []
    one_solution = []
    two_solutions = []
    three_solutions = []
    four_solutions = []
    inf_solutions = []
    for file in files:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                coefficients = list(map(int, line.split()))

                if len(coefficients) == 5:
                    eq = BiquadraticEquation(coefficients[0], coefficients[2], coefficients[4])

                    equations.append(eq)
                elif len(coefficients) == 3:
                    eq = QuadraticEquation(coefficients[0], coefficients[1], coefficients[2])
                    equations.append(eq)
                elif len(coefficients) == 2:
                    eq = Equation(coefficients[0], coefficients[1])
                    equations.append(eq)

    min_solution = float("-inf")
    max_solution = float("-inf")
    for equation in equations:
        solutions = equation.solve()
        if len(solutions) == 0:
            zero_solutions.append(equation)
        if len(solutions) == 1:
            if solutions[0] == float("inf"):
                inf_solutions.append(equation)
            else:
                one_solution.append(equation)
        elif len(solutions) == 2:
            two_solutions.append(equation)
        elif len(solutions) == 3:
            three_solutions.append(equation)
        elif len(solutions) == 4:
            four_solutions.append(equation)
        for solution in solutions:
            if (min_solution == float("-inf") or solution < min_solution) and solution != float("inf"):
                min_solution = solution
            if (max_solution == float("-inf") or solution > max_solution) and solution != float("inf"):
                max_solution = solution

    for equation in zero_solutions:
        equation.show()






