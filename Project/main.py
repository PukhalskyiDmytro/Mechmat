import tkinter as tk
from math import cos, sin, radians, sqrt
from abc import ABC, abstractmethod

WIDTH = 800
HEIGHT = 600
g = 9.81
TIME_STEP = 0.075

class Collision:
    def __init__(self, position, half_size):
        self.position = position
        self.size = half_size

    def check_hit(self, collision):
        delta_pos = self.position - collision.position

        return (abs(delta_pos.real) <= self.size.real + collision.size.real and
                abs(delta_pos.imag) <= self.size.imag + collision.size.imag)

class Object(ABC):
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.is_active = True
        self.collision = Collision(position, size)

    @abstractmethod
    def update(self, canvas):
        pass

    @abstractmethod
    def on_collision(self, another):
        pass

class Rectangle(Object):
    def __init__(self, position, size, color="gray"):
        self.size = size
        self.color = color
        super().__init__(position, size)

    def update(self, canvas):
        x0 = self.position.real - self.size.real
        y0 = HEIGHT - self.position.imag - self.size.imag
        x1 = self.position.real + self.size.real
        y1 = HEIGHT - self.position.imag + self.size.imag

        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)

    def on_collision(self, another):
        pass

class Projectile(Object):
    def __init__(self, position, velocity, radius=5, color="gray"):
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.time_elapsed = 0

        super().__init__(position, complex(radius, radius))

    def update(self, canvas):
        if not self.is_active:
            return

        dx = self.velocity.real * self.time_elapsed
        dy = self.velocity.imag * self.time_elapsed - (g * self.time_elapsed ** 2) / 2

        self.position += complex(dx, dy)

        self.time_elapsed += TIME_STEP
        if self.position.imag < 0:
            self.is_active = False

        x0 = self.position.real - self.radius
        y0 = HEIGHT - self.position.imag - self.radius
        x1 = self.position.real + self.radius
        y1 = HEIGHT - self.position.imag + self.radius

        canvas.create_oval(x0, y0, x1, y1, fill=self.color)
        self.collision.position = self.position

    def on_collision(self, another):
        self.is_active = False

class Tank(Object):
    def __init__(self, position, velocity = complex(0,0), trajectory = complex(0, 1), color="gray", size = complex(30, 30)):
        self.trajectory = trajectory
        self.velocity = velocity
        self.collision = Collision(position, size)
        self.size = size
        self.color = color
        self.on_ground = False
        self.time_in_air = 0
        self.projectiles = []
        self.prohibited_velocity = None
        super().__init__(position, size)

    def change_trajectory(self, event):
        if event.keysym == "w" or event.keysym == "s":
            a = radians(3) if event.keysym == "s" else radians(-3)
            self.trajectory *= complex(cos(a), sin(a))
        else:
            self.trajectory *= 21 / 22 if event.keysym == "Down" else 22 / 21

    def change_velocity(self, event):
        if self.on_ground:
            self.velocity = 3 if event.keysym == "d" else -3

    def fire(self):
        norm_trajectory = self.trajectory / sqrt(self.trajectory.real ** 2 + self.trajectory.imag ** 2) * 100
        return Projectile(position=self.position + norm_trajectory, velocity=self.trajectory, color=self.color)

    def update(self, canvas):
        if not self.is_active:
            return

        for projectile in self.projectiles:
            projectile.update(canvas)
            if not projectile.is_active:
                self.projectiles.remove(projectile)

        canvas.create_rectangle(self.position.real - self.size.real, HEIGHT - self.position.imag - self.size.imag,
                                self.position.real + self.size.real, HEIGHT - self.position.imag + self.size.imag,
                                fill=self.color)

        norm_trajectory = self.trajectory / sqrt(self.trajectory.real ** 2 + self.trajectory.imag ** 2) * 100
        canvas.create_line(self.position.real, HEIGHT - self.position.imag,
                           self.position.real + norm_trajectory.real,
                           HEIGHT - self.position.imag - norm_trajectory.imag, arrow=tk.LAST)
        self.collision.position = self.position
        self.velocity -= complex(0, (g * self.time_in_air ** 2) / 2)
        if self.prohibited_velocity is None or abs(self.velocity.real * self.prohibited_velocity.imag - self.velocity.imag * self.prohibited_velocity.real) < 0.1:
            self.position += self.velocity
        self.velocity = 0
        if not self.on_ground:
            self.time_in_air += TIME_STEP
        if self.position.imag < 0:
            self.is_active = False

    def on_collision(self, another):
        if isinstance(another, Projectile):
            self.is_active = False
        elif isinstance(another, Projectile):
            self.on_ground = True
            self.prohibited_velocity = self.position - another.position
            self.time_in_air = 0

class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg='lightblue')
        self.canvas.pack()

        self.objects: list[Object] = [Tank(complex(600, 200), color="blue"),
                        Tank(complex(200, 200), color="orange"),
                        Rectangle(complex(200,100), complex(100, 25), color="sienna"),
                        Rectangle(complex(600,100), complex(100, 25), color="sienna"),
                        Rectangle(complex(400,200), complex(25, 100), color="sienna")]

        self.current_player_index = 0

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

    def on_keyboard_interrupt(self, event):
        if event.keysym == "f":
            self.objects.append(self.objects[self.current_player_index].fire())

            players_indices = [i for i, obj in enumerate(self.objects) if isinstance(obj, Tank)]
            after_current = [i for i in players_indices if i > self.current_player_index]
            self.current_player_index = min(after_current) if after_current else min(players_indices)

        elif event.keysym == "a" or event.keysym == "d":
            self.objects[self.current_player_index].change_velocity(event)
        else:
            self.objects[self.current_player_index].change_trajectory(event)

    def update(self):
        self.canvas.delete('all')

        for i in range(len(self.objects)):
            self.objects[i].update(self.canvas)
            if isinstance(self.objects[i], Tank):
                pass
            for j in range(len(self.objects)):
                if self.objects[i].collision.check_hit(self.objects[j].collision) and i != j:
                    self.objects[i].on_collision(self.objects[j])
                    print(1)

        self.objects = [obj for obj in self.objects if obj.is_active]
        self.root.after(10, self.update)

    def run(self):
        self.update()
        self.root.mainloop()

if __name__ == '__main__':
    GameController().run()