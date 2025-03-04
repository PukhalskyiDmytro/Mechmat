from math import sqrt
from equation import Equation

class QuadraticEquation(Equation):
    def __init__(self, a, b, c):
        super().__init__(b, c)
        self.a = a
        self.b = b
        self.c = c

    def solve(self):
        if self.a == 0:
            return super().solve()

        discriminant = self.b**2 - 4 * self.a * self.c

        if discriminant < 0:
            return tuple()

        x_1 = (-self.b + sqrt(discriminant))/(2*self.a)
        x_2 = (-self.b - sqrt(discriminant))/(2*self.a)

        if discriminant > 0:
            return (x_1, x_2)
        elif discriminant == 0:
            return (x_1,)

    def show(self):
        b_str = self.b if self.b >= 0 else f"({self.b})"
        c_str = self.c if self.c >= 0 else f"({self.c})"
        print(f"{self.a}x^2 + {self.b}x + {self.c} = 0")

if __name__ == "__main__":
    eq = QuadraticEquation(1, 5, 4)
    print(eq.solve())