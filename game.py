import tkinter as tk
import random

WIDTH = 600
HEIGHT = 800
LANES = [150, 300, 450]

class CarGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="gray20")
        self.canvas.pack()

        self.player_lane = 1
        self.player = self.create_car(LANES[self.player_lane], 700, "red")

        self.obstacles = []
        self.speed = 10
        self.score = 0

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.spawn_obstacle()
        self.update()

    def create_car(self, x, y, color):
        parts = []

        # Main body
        parts.append(self.canvas.create_rectangle(x-30, y-50, x+30, y+50, fill=color, outline="black"))

        # Windshield
        parts.append(self.canvas.create_rectangle(x-20, y-40, x+20, y-10, fill="skyblue"))

        # Wheels
        parts.append(self.canvas.create_oval(x-35, y-40, x-25, y-20, fill="black"))
        parts.append(self.canvas.create_oval(x+25, y-40, x+35, y-20, fill="black"))
        parts.append(self.canvas.create_oval(x-35, y+20, x-25, y+40, fill="black"))
        parts.append(self.canvas.create_oval(x+25, y+20, x+35, y+40, fill="black"))

        return parts

    def move_car(self, car, dx, dy):
        for part in car:
            self.canvas.move(part, dx, dy)

    def set_car_position(self, car, x, y):
        coords = self.canvas.coords(car[0])
        cx = (coords[0] + coords[2]) / 2
        cy = (coords[1] + coords[3]) / 2
        dx = x - cx
        dy = y - cy
        self.move_car(car, dx, dy)

    def move_left(self, event):
        if self.player_lane > 0:
            self.player_lane -= 1
            self.set_car_position(self.player, LANES[self.player_lane], 700)

    def move_right(self, event):
        if self.player_lane < 2:
            self.player_lane += 1
            self.set_car_position(self.player, LANES[self.player_lane], 700)

    def spawn_obstacle(self):
        lane = random.randint(0, 2)
        x = LANES[lane]
        car = self.create_car(x, -100, random.choice(["white", "blue", "yellow"]))
        self.obstacles.append(car)
        self.root.after(1500, self.spawn_obstacle)

    def update(self):
        for car in self.obstacles[:]:
            self.move_car(car, 0, self.speed)

            if self.check_collision(car):
                self.game_over()
                return

            coords = self.canvas.coords(car[0])
            if coords[1] > HEIGHT:
                for part in car:
                    self.canvas.delete(part)
                self.obstacles.remove(car)
                self.score += 1

        self.canvas.delete("score")
        self.canvas.create_text(80, 30, text=f"Score: {self.score}",
                                fill="white", font=("Arial", 20), tag="score")

        self.root.after(50, self.update)

    def check_collision(self, car):
        x1, y1, x2, y2 = self.canvas.coords(car[0])
        px1, py1, px2, py2 = self.canvas.coords(self.player[0])
        return not (x2 < px1 or x1 > px2 or y2 < py1 or y1 > py2)

    def game_over(self):
        self.canvas.create_text(WIDTH//2, HEIGHT//2,
                                text="GAME OVER",
                                fill="red",
                                font=("Arial", 40))

root = tk.Tk()
root.title("Car Game")
game = CarGame(root)
root.mainloop()