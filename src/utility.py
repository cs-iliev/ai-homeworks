import math
from collections import deque
import queue


def is_square(number):
    root = math.sqrt(number)
    if int(root + 0.5) ** 2 == number:
        return True
    else:
        return False


def flatten_list(input_list):
    result = []
    for i in input_list:
        result.extend(i)

    return result


def is_even(num):
    return num % 2 == 0


class CustomQueue:
    """A custom queue that stores all nodes 
    that have been found in the search tree"""

    def __init__(self):
        self.queue = deque()

    def __contains__(self, item):
        for element in self.queue:
            if item.state == element.state:
                return True

        return False


class CustomStack:
    """A custom stack that stores all nodes that have already been explored"""

    def __init__(self):
        self.set = set()

    def __contains__(self, item):
        for element in self.set:
            if item.state == element.state:
                return True

        return False


class CustomPriorityQueue:
    """A custom priority queue where the position of elements is determined by heuristic"""

    def __init__(self):
        self.queue = queue.PriorityQueue()

    def __contains__(self, item):
        for element in self.queue:
            if item.state == element.state:
                return True

        return False
