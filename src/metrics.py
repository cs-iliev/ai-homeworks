import time


class Metrics:

    def __init__(self):
        self.path_to_goal = []
        self.nodes_expanded = 0
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
