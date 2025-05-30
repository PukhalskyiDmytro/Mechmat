from tkinter import PhotoImage
import tkinter as tk
from math import cos, sin, atan2, degrees
from abc import ABC, abstractmethod

WIDTH = 800
HEIGHT = 600
g = 9.81
TIME_STEP = 0.0075
SPEED = 0.5
ROTATION_SPEED = 0.005
ADD_POWER_SPEED = 1.0075
MAX_POWER = 15
TIME_BETWEEN_SHOTS = 0.8

def angle_from_vector(vector: complex):
    x, y = vector.real, vector.imag
    angle_rad = atan2(-y, x)
    angle_deg = degrees(angle_rad)
    return angle_deg

def sign(x):
    return (x > 0) - (x < 0)

def dot(v1: complex, v2: complex) -> float:
    return v1.real * v2.real + v1.imag * v2.imag

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
    def __init__(self, position, direction, size, color="gray"):
        self.color = color
        self.direction = direction
        self.collision = Collision(position, size)
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
    def __init__(self, position, direction, radius=5, color="gray"):
        self.time_elapsed = 0

        super().__init__(position, direction, complex(radius, radius), color)

    def update(self, **kwargs):
        dx = self.direction.real * self.time_elapsed
        dy = self.direction.imag * self.time_elapsed - (g * self.time_elapsed ** 2) / 2

        self.position += complex(dx, dy)
        self.time_elapsed += TIME_STEP
        self.collision.position = self.position

        for another in self.collision.objects_that_overlap:
            if isinstance(another, Rectangle) or isinstance(another, Projectile):
                self.is_active = False

        self.collision.update()

    def draw(self, canvas):
        x0 = self.position.real - self.size.real
        y0 = HEIGHT - self.position.imag - self.size.imag
        x1 = self.position.real + self.size.real
        y1 = HEIGHT - self.position.imag + self.size.imag

        canvas.create_oval(x0, y0, x1, y1, fill=self.color)

class Tank(GameObject):
    def __init__(self, position, direction = complex(0,0), trajectory = complex(0, 4),
                 color="gray", size = complex(40, 30), is_first=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.trajectory = trajectory
        self.time_in_air = 0
        self.time_from_last_shot = 1
        self.tank_sprite = PhotoImage(file='tank_simple.png')
        self.is_first = is_first

        super().__init__(position, direction, size, color)

    def keyboard_interrupt(self, pressed_keys):
        result = None

        if self.fire_key in pressed_keys:
            if self.time_from_last_shot >= TIME_BETWEEN_SHOTS:
                self.time_from_last_shot = 0
                return Projectile(position=self.position + normalize(self.trajectory)*100+complex(0, 15), direction=self.trajectory, color=self.color)

        if self.time_in_air == 0:
            if self.forward_key in pressed_keys:
                self.direction = SPEED
            if self.back_key in pressed_keys:
                self.direction = -SPEED
        if self.up_key in pressed_keys:
            self.trajectory *= complex(cos(ROTATION_SPEED), sin(ROTATION_SPEED))
        if self.down_key in pressed_keys:
            self.trajectory *= complex(cos(ROTATION_SPEED), -sin(ROTATION_SPEED))
        if self.more_power_key in pressed_keys:
            if abs(self.trajectory) < MAX_POWER:
                self.trajectory *= ADD_POWER_SPEED
        if self.less_power_key in pressed_keys:
            self.trajectory *= 1/ADD_POWER_SPEED

        return result

    def update(self):
        self.time_in_air += TIME_STEP

        for another in self.collision.objects_that_overlap:
            if isinstance(another, Projectile):
                self.is_active = False
            elif isinstance(another, Rectangle):
                for obstacle in self.collision.objects_that_overlap:
                    obstacle_dir = complex(0, 0)

                    x_in_range = self.position.real - self.size.real <= obstacle.position.real <= self.position.real + self.size.real
                    y_in_range = self.position.imag - self.size.imag <= obstacle.position.imag <= self.position.imag + self.size.imag

                    if x_in_range:
                        obstacle_dir = complex(0, 1 if obstacle.position.imag >= self.position.imag else -1)
                    elif y_in_range:
                        obstacle_dir = complex(1 if obstacle.position.real >= self.position.real else -1, 0)
                    else:
                        right = obstacle.position.real > self.position.real + self.size.real
                        smaller = obstacle.size.real <= self.size.real

                        if right:
                            obstacle_dir = complex(1, 0) if smaller else complex(0, -1)
                        else:
                            obstacle_dir = complex(0, -1) if obstacle.size.real > self.size.real else complex(-1, 0)

                    if obstacle_dir == complex(0, -1):
                        self.direction = self.direction.real
                        self.time_in_air = 0
                    elif dot(self.direction, obstacle_dir) >= 0:
                        self.direction = self.direction.imag

        self.direction -= complex(0, (g * self.time_in_air ** 2) / 2)
        self.position += self.direction
        self.direction = 0
        self.collision.position = self.position
        self.collision.update()
        self.time_from_last_shot += TIME_STEP

    def draw(self, canvas):
        canvas.create_line(self.position.real, HEIGHT-self.position.imag-15, (self.position+normalize(self.trajectory)*100).real,
                           HEIGHT-(self.position+normalize(self.trajectory)*100).imag-15, width=3, fill=self.color)

        canvas.create_image(self.position.real+4, HEIGHT-self.position.imag, image=self.tank_sprite)

        for i in range(int(abs(self.trajectory) * 4) // MAX_POWER+1):
            cx = 50 + i * 20 if self.is_first else WIDTH - (50 + i * 20)
            cy = 50
            canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=self.color)

class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tank game")
        self.root.iconbitmap("icon.ico")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg='lightblue')
        self.canvas.pack()

        self.first_player = Tank(complex(300, 400), color="navy",
                                 fire_key="Shift_L", forward_key="d", back_key="a", more_power_key="r",
                                 less_power_key="f", up_key="w", down_key="s")
        self.second_player = Tank(complex(500, 400), color="deep pink", is_first = False,
                                  fire_key="j", forward_key = "Right", back_key = "Left", more_power_key="i",
                                  less_power_key = "k", up_key="Down", down_key = "Up")

        self.objects: list[GameObject] = [self.first_player, self.second_player]

        self.pressed_keys = set()
        self.is_running = False

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

    def on_key_press(self, event):
        self.pressed_keys.add(event.keysym)

    def on_key_release(self, event):
        self.pressed_keys.discard(event.keysym)

    def update(self):
        self.canvas.delete('all')
        self.objects = [obj for obj in self.objects if obj.is_active]

        r1 = self.first_player.keyboard_interrupt(self.pressed_keys)
        r2 = self.second_player.keyboard_interrupt(self.pressed_keys)

        if r1 is not None:
            self.objects.append(r1)
        if r2 is not None:
            self.objects.append(r2)

        for i in range(len(self.objects)):
            self.objects[i].update()
            self.objects[i].draw(self.canvas)

            for j in range(i + 1, len(self.objects)):
                obj1 = self.objects[i]
                obj2 = self.objects[j]

                obj1.collision.check_hit(obj2)
                obj2.collision.check_hit(obj1)

            if not (self.objects[i].position.imag > 0 and 0 < self.objects[i].position.real < WIDTH):
                self.objects[i].is_active = False

            if self.objects[i].is_active == False and isinstance(self.objects[i], Tank):
                self.game_over()

        if self.is_running:
            self.root.after(1, self.update)

    def add_game_object(self, obj: GameObject):
        self.objects.append(obj)

    def extend_game_objects(self, objs: list[GameObject]):
        self.objects.extend(objs)

    def run(self):
        self.is_running = True
        self.update()
        self.root.mainloop()

    def game_over(self):
        self.is_running = False
        text = f"Game Over! {self.first_player.color.upper() if self.first_player.is_active == True else self.second_player.color.upper()} tank wins!"
        self.canvas.create_text(WIDTH // 2, 100,
                                text=text, fill="black", font=("Arial", 24), )

if __name__ == '__main__':
    c = GameController()
    c.extend_game_objects([ Rectangle(complex(400, 360), complex(50, 100)),
                            Rectangle(complex(400, 260), complex(50, 50)),
                            Rectangle(complex(300, 230), complex(25, 50)),
                            Rectangle(complex(300, 100), complex(25, 35)),
                            Rectangle(complex(500, 100), complex(25, 35)),
                            Rectangle(complex(500, 230), complex(25, 50)),
                            Rectangle(complex(400, 275), complex(225, 50)),
                            Rectangle(complex(125, 450), complex(100, 30)),
                            Rectangle(complex(800-125, 450), complex(100, 30)),
                            Rectangle(complex(175, 75), complex(150, 30)),
                            Rectangle(complex(625, 75), complex(150, 30)),
                            ])
    c.run()
