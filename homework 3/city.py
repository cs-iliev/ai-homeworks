import math


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        dist_x = abs(self.x - city.x)
        dist_y = abs(self.y - city.y)
        distance = math.sqrt((dist_x ** 2) + (dist_y ** 2))
        return distance

    def print(self):
        print(f'({self.x}, {self.y})')
