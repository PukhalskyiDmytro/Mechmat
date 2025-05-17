import tkinter as tk
from math import cos, sin, radians

class Object:
    def __init__(self, coordinates: complex):
        self.coordinates = coordinates
        self.is_active = True

    def update(self, canvas: tk.Canvas):
        pass

class CollisionDetector:
    def __init__(self, coordinates, width, height):
        self.coordinates = coordinates
        self.width = width
        self.height = height

    def check_hit(self, object_coordinates: complex) -> bool:
        return abs(object_coordinates.real - self.coordinates.real) <= self.width and abs(object_coordinates.imag - self.coordinates.imag) <= self.height

class Projectile(Object):
    def __init__(self, coordinates: complex, velocity: complex, radius = 5, color = "gray"):
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.dt = 0
        super().__init__(coordinates)

    def update(self, canvas):
        if self.is_active:
            self.coordinates += complex(self.velocity.real * self.dt, self.velocity.imag * self.dt - (9.81 * self.dt ** 2)/2)
            self.dt += 0.075
            if self.coordinates.imag < 0:
                self.is_active = False

            canvas.create_oval(self.coordinates.real - self.radius, 600 - self.coordinates.imag - self.radius,
                            self.coordinates.real + self.radius, 600 - self.coordinates.imag + self.radius,
                            fill=self.color)

class Tank(Object):
    def __init__(self, coordinates: complex, velocity: complex = complex(0, 3), color = "gray", width = 30, height = 30):
        self.velocity = velocity
        self.collision = CollisionDetector(coordinates,width, height)
        self.width = width
        self.height = height
        self.color = color
        self.projectiles = []
        super().__init__(coordinates)

    def change_velocity(self, event):
        if event.keysym == "Right" or event.keysym == "Left":
            a = radians(3) if event.keysym == "Left" else radians(-3)
            self.velocity *= complex(cos(a), sin(a))
        else:
            self.velocity *= 21/22 if event.keysym == "Down" else 22/21

    def fire(self):
        self.projectiles.append(Projectile(coordinates=self.coordinates+10*self.velocity, velocity=self.velocity, color=self.color))

    def update(self, canvas):
        if self.is_active:
            for index, projectile in enumerate(self.projectiles):
                projectile.update(canvas)
                if not projectile.is_active:
                    self.projectiles.pop(index)
            canvas.create_rectangle(self.coordinates.real-self.width, 600-self.coordinates.imag-self.height, self.coordinates.real+self.width, 600-self.coordinates.imag+self.height, fill=self.color)
            canvas.create_line(self.coordinates.real, 600 - self.coordinates.imag,
                               self.coordinates.real + self.velocity.real*10,
                               600 - self.coordinates.imag - self.velocity.imag*10, arrow=tk.LAST)


class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='lightblue')
        self.canvas.pack()

        self.players = [Tank(complex(600, 200), color="blue"), Tank(complex(200, 200), color="orange")]
        self.current_player_index = 0

        self.root.bind("<Left>", self.on_keyboard_interrupt)
        self.root.bind("<Right>", self.on_keyboard_interrupt)
        self.root.bind("<Up>", self.on_keyboard_interrupt)
        self.root.bind("<Down>", self.on_keyboard_interrupt)
        self.root.bind("<f>", self.on_keyboard_interrupt)

    def on_keyboard_interrupt(self, event):
        if event.keysym == "f":
            self.players[self.current_player_index].fire()
            self.current_player_index += 1
            if self.current_player_index >= len(self.players):
                self.current_player_index = 0
        else:
            self.players[self.current_player_index].change_velocity(event)

    def update(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 600-20, 800, 600, fill='sienna')

        for index, player_1 in enumerate(self.players):
            for player_2 in self.players:
                for projectile in player_1.projectiles:
                    if player_2.collision.check_hit(projectile.coordinates):
                        player_2.is_active = False
                        projectile.is_active = False
            player_1.update(self.canvas)
            if not player_1.is_active:
                self.players.pop(index)

        self.root.after(10, self.update)

    def run(self):
        self.update()
        self.root.mainloop()

if __name__ == '__main__':
    GameController().run()