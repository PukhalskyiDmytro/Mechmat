class Equation:
    def __init__(self, b, c):
        self.b = b
        self.c = c

    def solve(self):
        if self.b == 0:
            if self.c == 0:
                return (float("inf"),)
            return tuple()
        return (-self.c/self.b,)

    def show(self):
        c_str = self.c if self.c >= 0 else f"({self.c})"
        print(f"{self.b}x + {c_str} = 0")

if __name__ == "__main__":
    eq = Equation(1, -5)
    print(eq.solve())