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
    def __new__(cls, side1, side2, side3):
        if side1 <= 0 or side2 <= 0 or side3 <= 0:
            return None
        if side1 + side2 <= side3 or side1 + side3 <= side2 or side2 + side3 <= side1:
            return None
        return super().__new__(cls)

    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def area(self):
        semi_perimeter = self.perimeter() / 2
        return sqrt(semi_perimeter * (semi_perimeter - self.side1) * (semi_perimeter - self.side2) * (semi_perimeter - self.side3))

    def perimeter(self):
        return self.side1 + self.side2 + self.side3

    def type(self):
        return "triangle"

class Rectangle(Figure):
    def __new__(cls, width, height):
        if width <= 0 or height <= 0:
            return None
        return super().__new__(cls)

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def type(self):
        return "rectangle"

class Circle(Figure):
    def __new__(cls, radius):
        if radius <= 0:
            return None
        return super().__new__(cls)

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2

    def perimeter(self):
        return 2 * pi * self.radius

    def type(self):
        return "circle"

class Parallelogram(Figure):
    def __new__(cls, base, side, height):
        if base <= 0 or side <= 0 or height <= 0:
            return None
        return super().__new__(cls)

    def __init__(self, base, side, height):
        self.base = base
        self.side = side
        self.height = height

    def area(self):
        return self.base * self.height

    def perimeter(self):
        return 2 * (self.base + self.side)

    def type(self):
        return "parallelogram"

class Trapeze(Figure):
    def __new__(cls, base1, base2, leg1, leg2):
        semi_perimeter = (base1 + base2 + leg1 + leg2) / 2
        expr = (semi_perimeter - base1) * (semi_perimeter - base2) * ((semi_perimeter - base1 - leg1) * (semi_perimeter - base1 - leg2)) / semi_perimeter

        if base1 <= 0 or base2 <= 0 or leg1 <= 0 or leg2 <= 0 or expr < 0:
            return None

        return super().__new__(cls)

    def __init__(self, base1, base2, leg1, leg2):
        self.base1 = base1
        self.base2 = base2
        self.leg1 = leg1
        self.leg2 = leg2

    def perimeter(self):
        return self.base1 + self.base2 + self.leg1 + self.leg2

    def area(self):
        semi_perimeter = self.perimeter() / 2
        expr = (semi_perimeter - self.base1) * (semi_perimeter - self.base2) * ((semi_perimeter - self.base1 - self.leg1) * (semi_perimeter - self.base1 - self.leg2)) / semi_perimeter
        height = (2 / abs(self.base1 - self.base2)) * sqrt(expr)
        return 0.5 * (self.base1 + self.base2) * height

    def type(self):
        return "trapeze"

if __name__ == "__main__":
    max_area_shape = None
    max_perimeter_shape = None

    min_area_shape = None
    min_perimeter_shape = None

    for index in range(1, 4):
        with open(f"input0{index}.txt", 'r') as input_file:
            for line_data in input_file:
                tokens = line_data.strip().split()
                shape_type = tokens[0]
                parameters = list(map(float, tokens[1:]))

                shape = None

                if shape_type == "Rectangle":
                    shape = Rectangle(parameters[0], parameters[1])
                elif shape_type == "Triangle":
                    shape = Triangle(parameters[0], parameters[1], parameters[2])
                elif shape_type == "Circle":
                    shape = Circle(parameters[0])
                elif shape_type == "Parallelogram":
                    shape = Parallelogram(parameters[0], parameters[1], parameters[2])
                elif shape_type == "Trapeze":
                    if parameters[0] == parameters[2]:
                        shape = Rectangle(parameters[0], parameters[2])
                    else:
                        shape = Trapeze(parameters[0], parameters[1], parameters[2], parameters[3])

                if shape is not None:
                    if max_area_shape is None or max_area_shape.area() < shape.area():
                        max_area_shape = shape
                    if max_perimeter_shape is None or max_perimeter_shape.perimeter() < shape.perimeter():
                        max_perimeter_shape = shape
                    if min_area_shape is None or min_area_shape.area() > shape.area():
                        min_area_shape = shape
                    if min_perimeter_shape is None or min_perimeter_shape.perimeter() > shape.perimeter():
                        min_perimeter_shape = shape

    print("Perimeters")
    print(f"Max perimeter has {max_perimeter_shape.type()} and it's {max_perimeter_shape.perimeter()}")
    print(f"Min perimeter has {min_perimeter_shape.type()} and it's {min_perimeter_shape.perimeter()}")

    print("Areas")
    print(f"Max area has {max_area_shape.type()} and it's {max_area_shape.area()}")
    print(f"Min area has {min_area_shape.type()} and it's {min_area_shape.area()}")
