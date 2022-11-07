import time


class Metrics:

    def __init__(self):
        self.path_to_goal = []
        self.start_time = 0
        self.end_time = 0
        self.search_time = 0

    def cost_of_path(self):
        return len(self.path_to_goal)

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        self.end_time = time.time()
        self.search_time = "{0:.5f} ms".format(
            (self.end_time - self.start_time) * 1000)

    def display(self):
        print('Cost of path is: ', self.cost_of_path())
        print('Path: ', self.path_to_goal)
        print('Search time: ', self.search_time)
