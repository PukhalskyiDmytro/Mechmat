from abc import ABC, abstractmethod
from math import sqrt, pi

class Figure(ABC):
    @abstractmethod
    def area(self):
        return 0

    @abstractmethod
    def perimeter(self):
        return 0

    @abstractmethod
    def type(self):
        return ""

class Triangle(Figure):
    def __new__(cls, a, b, c):
        if a <= 0 or b <= 0 or c <= 0:
            return None
        if a + b <= c or a + c <= b or b + c <= a:
            return None

        return super().__new__(cls)

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        p = self.perimeter()/2
        area = sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
        return area

    def perimeter(self):
        return self.a + self.b + self.c

    def type(self):
        return "triangle"

class Rectangle(Figure):
    def __new__(cls, a, b):
        if a <= 0 or b <= 0:
            return None

        return super().__new__(cls)

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def area(self):
        return self.a * self.b

    def perimeter(self):
        return 2*(self.a+self.b)

    def type(self):
        return "rectangle"

class Circle(Figure):
    def __new__(cls, r):
        if r <= 0:
            return None

        return super().__new__(cls)

    def __init__(self, r):
        self.r = r

    def area(self):
        return pi * self.r ** 2

    def perimeter(self):
        return 2 * pi * self.r

    def type(self):
        return "circle"

class Parallelogram(Figure):
    def __new__(cls, a, b, h):
        if a <= 0 or b <= 0 or h <= 0:
            return None

        return super().__new__(cls)

    def __init__(self, a, b, h):
        self.a = a
        self.b = b
        self.h = h  # до сторони a

    def area(self):
        return self.a*self.h

    def perimeter(self):
        return 2*(self.a + self.b)

    def type(self):
        return "parallelogram"

class Trapeze(Figure):
    def __new__(cls, a, b, c, d):
        s = (a + b + c + d) / 2
        expr = (s - a) * (s - c) * ((s - a - b) * (s - a - d)) / s

        if a <= 0 or b <= 0 or c <= 0 or d <= 0 or expr < 0:
            return None

        return super().__new__(cls)

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b # a та b паралельні
        self.c = c
        self.d = d

    def perimeter(self):
        return self.a+self.b+self.c+self.d

    def area(self):
        s = self.perimeter() / 2
        expr = (s - self.a) * (s - self.c) * ((s - self.a - self.b) * (s - self.a - self.d)) / s

        height = (2 / abs(self.a - self.c)) * sqrt(expr)
        area = 0.5 * (self.a + self.c) * height

        return area

    def type(self):
        return "trapeze"

if __name__ == "__main__":
    #Unit tests

    #print("Triangle")
    #triangle = Triangle(3, 4, 5)
    #print(t.area())
    #print(t.perimeter())

    #print("Rectangle")
    #rectangle = Rectangle(3, 4)
    #print(r.area())
    #print(r.perimeter())

    #print("Circle")
    #circle = Circle(5)
    #print(c.area())
    #print(c.perimeter())

    #print("Trapeze")
    #trapeze = Trapeze(7, 10, 5, 4)
    #print(tr.area())
    #print(tr.perimeter())

    max_area_figure = None
    max_perimeter_figure = None

    min_area_figure = None
    min_perimeter_figure = None

    for i in range(1,4):
        with open(f"input0{i}.txt", 'r') as file:
            for line in file:
                elements = line.strip().split()
                name = elements[0]
                args = list(map(float, elements[1:]))

                f = None

                if name == "Rectangle":
                    f = Rectangle(args[0], args[1])
                elif name == "Triangle":
                    f = Triangle(args[0], args[1], args[2])
                elif name == "Circle":
                    f = Circle(args[0])
                elif name == "Parallelogram":
                    f = Parallelogram(args[0], args[1], args[2])
                elif name == "Trapeze":
                    if args[0] == args[2]:
                        f = Rectangle(args[0], args[2])
                    else:
                        f = Trapeze(args[0], args[1], args[2], args[3])
                else:
                    f = None

                if f is not None:
                    if max_area_figure is None or max_area_figure.area() < f.area():
                        max_area_figure = f
                    if max_perimeter_figure is None or max_perimeter_figure.perimeter() < f.perimeter():
                        max_perimeter_figure = f

    print("Perimeters")
    print(f"Max perimeter has {max_perimeter_figure.type()} and it's {max_perimeter_figure.perimeter()}")

    print("Areas")
    print(f"Max area has {max_area_figure.type()} and it's {max_area_figure.area()}")