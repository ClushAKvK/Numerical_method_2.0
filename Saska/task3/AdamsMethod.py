import matplotlib.pyplot as plt
import numpy as np
from TestFunctions import *


func = None
ansFunc = None


class AdamsMethod:

    splits = 50

    def __init__(self, a, b, start):
        self.a = a
        self.b = b
        self.start = start
        self.step = abs(b - a) / self.splits

        self.system_count = len(start)
        self.dots = [[] for i in range(self.system_count)]

    def get_runge_kut_begin(self):
        begin_y = [[] for i in range(len(self.start))]

        h = 0.1
        y = self.start
        t = self.a

        for i in range(self.system_count):
            begin_y[i].append(y[i])
            self.dots.append((t, y[i]))

        while len(begin_y) < 5:
            t += self.step

            for i in range(self.system_count):
                tempF = eval(func[i])

                k1 = tempF(t, y)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + 0.5 * h * k1)
                k2 = tempF(t + 0.5 * h, params)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + 0.5 * h * k2)


def main():

    a = [[] for i in range(5)]
    a[0].append(1)

    with open('input1.txt') as fin:
        a, b = map(int, fin.readline().split())
        start = [c for c in fin.readline().split()]
        func = [f for f in fin.readline().split()]
        ansFunc = [f for f in fin.readline().split()]


if __name__ == "__main__":
    main()