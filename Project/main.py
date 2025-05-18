import tkinter as tk
from tkinter import messagebox
from math import cos, sin, radians, sqrt
from abc import ABC, abstractmethod

from sympy.physics.units import velocity

WIDTH = 800
HEIGHT = 600
g = 9.81
TIME_STEP = 0.0075

def sign(x):
    return (x > 0) - (x < 0)

def dot(v1: complex, v2: complex) -> float:
    return (v1.real * v2.real + v1.imag * v2.imag)

def cross(v1: complex, v2: complex):
    x1, y1 = v1.real, v1.imag
    x2, y2 = v2.real, v2.imag
    return x1 * y2 - y1 * x2

def normalize(v: complex) -> complex:
    if abs(v) == 0:
        return complex(0, 0)
    return v / abs(v)

class Object(ABC):
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.is_active = True

    @abstractmethod
    def update(self):
        pass

class Collision(Object):
    def __init__(self, position, half_size):
        self.overlap = False
        self.objects_that_overlap = []
        super().__init__(position, half_size)

    def update(self):
        self.objects_that_overlap.clear()

        self.overlap = False

    def check_hit(self, another):
        delta_pos = self.position - another.collision.position

        if (abs(delta_pos.real) <= self.size.real + another.collision.size.real and
                abs(delta_pos.imag) <= self.size.imag + another.collision.size.imag):
            self.overlap = True
            self.objects_that_overlap.append(another)

class GameObject(Object):
    id = 0
    def __init__(self, position, velocity, size, color="gray"):
        self.color = color
        self.velocity = velocity
        self.collision = Collision(position, size)
        self.id = GameObject.id
        GameObject.id += 1
        super().__init__(position, size)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, canvas):
        pass

class Rectangle(GameObject):
    def __init__(self, position, size, color="gray"):
        super().__init__(position, 0, size, color)

    def update(self):
        self.collision.update()

    def draw(self, canvas):
        x0 = self.position.real - self.size.real
        y0 = HEIGHT - self.position.imag - self.size.imag
        x1 = self.position.real + self.size.real
        y1 = HEIGHT - self.position.imag + self.size.imag

        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)

class Projectile(GameObject):
    def __init__(self, position, velocity, radius=5, color="gray"):
        self.time_elapsed = 0

        super().__init__(position, velocity, complex(radius, radius), color)

    def update(self):
        dx = self.velocity.real * self.time_elapsed
        dy = self.velocity.imag * self.time_elapsed - (g * self.time_elapsed ** 2) / 2

        self.position += complex(dx, dy)
        self.time_elapsed += TIME_STEP
        self.collision.position = self.position

        for another in self.collision.objects_that_overlap:
            if isinstance(another, Rectangle):
                self.is_active = False

        self.collision.update()

    def draw(self, canvas):
        x0 = self.position.real - self.size.real
        y0 = HEIGHT - self.position.imag - self.size.imag
        x1 = self.position.real + self.size.real
        y1 = HEIGHT - self.position.imag + self.size.imag

        canvas.create_oval(x0, y0, x1, y1, fill=self.color)

class Tank(GameObject):
    def __init__(self, position, velocity = complex(0,0), trajectory = complex(0, 4), color="gray", size = complex(30, 30)):
        self.trajectory = trajectory
        self.time_in_air = 0
        super().__init__(position, velocity, size, color)

    def change_trajectory(self, event):
        if event.keysym == "w" or event.keysym == "s":
            a = radians(3) if event.keysym == "s" else radians(-3)
            self.trajectory *= complex(cos(a), sin(a))
        else:
            self.trajectory *= 21 / 22 if event.keysym == "Down" else 22 / 21

    def change_velocity(self, event):
        self.velocity = 1 if event.keysym == "d" else -1

    def fire(self):
        norm_trajectory = self.trajectory / sqrt(self.trajectory.real ** 2 + self.trajectory.imag ** 2) * 100
        return Projectile(position=self.position + norm_trajectory, velocity=self.trajectory, color=self.color)

    def update(self):
        self.time_in_air += TIME_STEP
        self.velocity -= complex(0, (g * self.time_in_air ** 2) / 2)

        for another in self.collision.objects_that_overlap:
            if isinstance(another, Projectile):
                self.is_active = False
            elif isinstance(another, Rectangle):
                for obstacle in self.collision.objects_that_overlap:
                    obstacle_dir = complex(0, 0)

                    dx = obstacle.position.real - self.position.real
                    dy = obstacle.position.imag - self.position.imag
                    half_width = self.size.real
                    half_height = self.size.imag

                    if -half_width <= dx <= half_width:
                        obstacle_dir = complex(0, 1 if dy >= 0 else -1)
                    elif -half_height <= dy <= half_height:
                        obstacle_dir = complex(1 if dx >= 0 else -1, 0)
                    elif dy > half_height:
                        obstacle_dir = complex(
                            1 if dx > half_width >= obstacle.size.real else -1 if dx <= half_width and obstacle.size.real <= half_width else 0,
                            1
                        )
                    else:
                        obstacle_dir = complex(
                            1 if dx > half_width >= obstacle.size.real else -1 if obstacle.size.real <= half_width else 0,
                            -1 if dx <= half_width < obstacle.size.real else 0
                        )

                    if obstacle_dir == complex(0, -1):
                        self.velocity = self.velocity.real
                    elif dot(self.velocity, obstacle_dir) >= 0:
                        self.velocity = self.velocity.imag

        self.position += self.velocity
        self.velocity = 0
        self.collision.position = self.position
        self.collision.update()

    def draw(self, canvas):
        canvas.create_rectangle(self.position.real - self.size.real, HEIGHT - self.position.imag - self.size.imag,
                                self.position.real + self.size.real, HEIGHT - self.position.imag + self.size.imag,
                                fill=self.color)

        norm_trajectory = self.trajectory / sqrt(self.trajectory.real ** 2 + self.trajectory.imag ** 2) * 100

        canvas.create_line(self.position.real, HEIGHT - self.position.imag,
                           self.position.real + norm_trajectory.real,
                           HEIGHT - self.position.imag - norm_trajectory.imag, arrow=tk.LAST)

class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg='lightblue')
        self.canvas.pack()

        self.objects: list[GameObject] = [Tank(complex(600, 200), color="blue"),
                        Tank(complex(200, 200), color="orange"),
                        Rectangle(complex(200,100), complex(100, 25), color="sienna"),
                        Rectangle(complex(600,100), complex(100, 25), color="sienna"),
                        Rectangle(complex(525, 205), complex(25, 25), color="sienna"),
                        Rectangle(complex(400,250), complex(25, 100), color="sienna")]

        self.current_player_id = 0

        self.bind_keys()

    def bind_keys(self):
        self.root.bind("<Left>", self.on_keyboard_interrupt)
        self.root.bind("<Right>", self.on_keyboard_interrupt)
        self.root.bind("<Up>", self.on_keyboard_interrupt)
        self.root.bind("<Down>", self.on_keyboard_interrupt)
        self.root.bind("<f>", self.on_keyboard_interrupt)
        self.root.bind("<a>", self.on_keyboard_interrupt)
        self.root.bind("<d>", self.on_keyboard_interrupt)
        self.root.bind("<w>", self.on_keyboard_interrupt)
        self.root.bind("<s>", self.on_keyboard_interrupt)
        self.root.bind("<u>", self.on_keyboard_interrupt)

    def get_players(self):
        players = [i for i, obj in enumerate(self.objects) if isinstance(obj, Tank)]
        return players

    def on_keyboard_interrupt(self, event):
        if event.keysym == "f":
            self.objects.append(self.objects[self.current_player_id].fire())

            current_players = self.get_players()
            after_current = [i for i in current_players if i > self.current_player_id]
            self.current_player_id = min(after_current) if after_current else min(current_players)

        elif event.keysym == "a" or event.keysym == "d":
            self.objects[self.current_player_id].change_velocity(event)
        elif event.keysym == "u":
            pass
        else:
            self.objects[self.current_player_id].change_trajectory(event)

    def update(self):
        self.canvas.delete('all')

        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                obj1 = self.objects[i]
                obj2 = self.objects[j]

                obj1.collision.check_hit(obj2)
                obj2.collision.check_hit(obj1)

            self.objects[i].update()
            self.objects[i].draw(self.canvas)

        if len(self.get_players()) <= 1:
            self.root.destroy()

        self.objects = [obj for obj in self.objects if (obj.is_active and obj.position.imag > 0 and 0 < obj.position.real < WIDTH)]
        self.root.after(1, self.update)

    def run(self):
        self.update()
        self.root.mainloop()

if __name__ == '__main__':
    GameController().run()