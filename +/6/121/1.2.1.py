from math import sqrt

class QuadraticEquation:
    def __init__(self, a, b=0, c=0):
        if isinstance(a, QuadraticEquation):
            self.a = a.a
            self.b = a.b
            self.c = a.c
        else:
            self.a = a
            self.b = b
            self.c = c

    def solve(self):
        if self.a == 0:
            if self.b == 0:
                if self.c == 0:
                    return float("inf"), float('inf')
                else:
                    return 0, None
            else:
                return 1, -(self.c/self.b)
        else:
            discriminant = self.b**2 - 4*self.a*self.c

            if discriminant > 0:
                x_1 = (-self.b+sqrt(discriminant))/(2*self.a)
                x_2 = (-self.b-sqrt(discriminant))/(2*self.a)

                return 2, x_1, x_2
            elif discriminant == 0:
                x = (-self.b)/(2*self.a)
                return 1, x
            else:
                return 0, None

    def show(self):
        return f"{self.a}*x^2 + {self.b}*x + {self.c}"

if __name__ == "__main__":
    #Unit tests

    eq_1 = QuadraticEquation(0,0,0)

    #print(eq_1.show())
    #print(eq_1.solve())

    eq_2 = QuadraticEquation(0, 0, -7)

    #print(eq_2.show())
    #print(eq_2.solve())

    eq_3 = QuadraticEquation(0, 1, 1)

    #print(eq_3.show())
    #print(eq_3.solve())

    eq_4 = QuadraticEquation(1, 2, 0)

    #print(eq_4.show())
    #print(eq_4.solve())

    eq_5 = QuadraticEquation(1, 2, 1)

    #print(eq_5.show())
    #print(eq_5.solve())

    eq_6 = QuadraticEquation(1, 2, 2)

    #print(eq_6.show())
    #print(eq_6.solve())

    one_sol = []
    two_sol = []
    zero_sol = []
    inf_sol = []

    for i in range(1,4):
        with open(f"input0{i}.txt", 'r') as file:
            for line in file:
                a, b, c = map(int, line.split())
                eq = QuadraticEquation(a, b, c)
                print(eq.show())

                solutions = eq.solve()
                print(solutions[1:])

                if solutions[0] == 0:
                    zero_sol.append(eq)
                elif solutions[0] == 1:
                    one_sol.append(eq)
                elif solutions[0] == 2:
                    two_sol.append(eq)
                else:
                    inf_sol.append(eq)

    solutions = [eq.solve()[1] for eq in one_sol]
    print(f"Max: {max(solutions)}, min: {min(solutions)}")