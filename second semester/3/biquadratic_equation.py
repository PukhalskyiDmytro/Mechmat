from quadratic_equation import QuadraticEquation, Equation, sqrt

class BiquadraticEquation(QuadraticEquation):
    def __init__(self, a, b, c ):
        super().__init__(a, b, c)
        self.a = a
        self.b = b
        self.c = c

    def solve(self):
        solutions = tuple(super().solve())
        result = []
        for solution in solutions:
            if solution >= 0:
                result.append(sqrt(solution))
                result.append(-sqrt(solution))
            elif solution == float("inf"):
                result.append(solution)

        return tuple(result)

    def show(self):
        b_str = self.b if self.b >= 0 else f"({self.b})"
        c_str = self.c if self.c >= 0 else f"({self.c})"
        print(f"{self.a}x^4 + {b_str}x^2 + {c_str} = 0")

if __name__ == "__main__":
    eq = BiquadraticEquation(1, 5, 4)
    print(eq.solve())