from random import randint


class Box:
    def __init__(self, x, y):
        self.coords = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]

        self.TopLeft = (x, y)
        self.TopLine = (self.coords[0], self.coords[1])
        self.RightLine = (self.coords[1], self.coords[3])
        self.BottomLine = (self.coords[2],  self.coords[3])
        self.LeftLine = (self.coords[0],  self.coords[2])

        self.lines = ([self.TopLine, self.RightLine,
                      self.BottomLine, self.LeftLine])

        self.top = False
        self.bottom = False
        self.left = False
        self.right = False

        self.owner = None
        self.complete = False
        self.value = ' '

    def connect_dot(self, coords):
        success = False
        if coords in self.lines:
            if coords == self.TopLine and self.top is False:
                self.top = True
                success = True
            elif coords == self.BottomLine and self.bottom is False:
                self.bottom = True
                success = True
            elif coords == self.LeftLine and self.left is False:
                self.left = True
                success = True
            elif coords == self.RightLine and self.right is False:
                self.right = True
                success = True

        if self.top is True and self.bottom is True and self.left is True and self.Right is True:
            self.complete = True

        return success
