from random import random
from math import pi

class FindPI:
    def __init__(self):
        self.inside = 0
        self.total = 0
        self.radius = float(0.5)
        self.best = 0
        self.gap = 10

    def isInside(self, _x, _y):
        return (_x ** 2 + _y ** 2) < 1

    def estimatePI(self):
        result = (self.inside * 4) / self.total
        if float(abs(result - pi)) < float(self.gap):
            self.gap = float(abs(result - pi))
            self.best = result
        print('n = {}, best = {:.10f}, pi = {:.10f}'.format(self.total, self.best, result))

    def generate(self):
        while True:
            x = random()
            y = random()
            self.total += 1

            if self.isInside(x, y):
                self.inside += 1

            self.estimatePI()


getPI = FindPI()
getPI.generate()