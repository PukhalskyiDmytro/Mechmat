class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices

    def is_convex(self):
        n = len(self.vertices)
        if n < 3:
            return False

        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        sign = 0
        for i in range(n):
            o = self.vertices[i]
            a = self.vertices[(i + 1) % n]
            b = self.vertices[(i + 2) % n]
            cp = cross_product(o, a, b)
            if cp != 0:
                if sign == 0:
                    sign = 1 if cp > 0 else -1
                elif (cp > 0 > sign) or (sign > 0 > cp):
                    return False
        return True


class Pentagon(Polygon):
    def __init__(self, vertices):
        if len(vertices) != 5:
            raise ValueError("This polygon must have 5 verticies")
        super().__init__(vertices)

class Hexagon(Polygon):
    def __init__(self, vertices):
        if len(vertices) != 6:
            raise ValueError("This polygon must have 6 vertices")
        super().__init__(vertices)

if __name__ == "__main__":
    polygons = []
    with open("polygons.txt", 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            n = int(lines[i])
            i += 1
            vertices = []
            for _ in range(n):
                x, y = map(float, lines[i].split())
                vertices.append((x, y))
                i += 1
            if n == 5:
                polygon = Pentagon(vertices)
            elif n == 6:
                polygon = Hexagon(vertices)
            else:
                polygon = Polygon(vertices)
            polygons.append(polygon)

    convex_polygons = [poly for poly in polygons if poly.is_convex()]

    print(f"Number of convex polygons: {len(convex_polygons)}")
    for i, poly in enumerate(convex_polygons, start=1):
        print(f"№{i}. Convex polygon: {poly.vertices}")
