import matplotlib.pyplot as plt
import numpy as np
from TestFunctions import *

func = None
ansFunc = None


class AdamsMethod:

    splits = 10

    def __init__(self, a, b, start):
        self.a = a
        self.b = b
        self.start = start
        self.step = abs(b - a) / self.splits

        self.system_count = len(start)
        self.dots = [[] for i in range(self.system_count)]

    def get_runge_kut_begin(self):
        begin_y = [[] for i in range(len(self.start))]

        h = self.step
        y = self.start
        newY = []
        t = self.a

        for i in range(self.system_count):
            begin_y[i].append(y[i])
            self.dots[i].append((t, y[i]))

        while len(begin_y[0]) < 5:
            # print(t)
            t += self.step

            for i in range(self.system_count):
                tempF = eval(*func[i])

                k1 = tempF(t, y)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + 0.5 * h * k1)
                k2 = tempF(t + 0.5 * h, params)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + 0.5 * h * k2)
                k3 = tempF(t + 0.5 * h, params)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + h * k3)
                k4 = tempF(t + h, params)

                # ~~~
                ny = y[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
                newY.append(ny)
                begin_y[i].append(ny)
                self.dots[i].append((t, ny))

            y = newY

        print(*self.dots, sep='\n')


def main():

    a = [[] for i in range(5)]
    a[0].append(1)

    with open('input1.txt') as fin:
        a, b = map(float, fin.readline().split())
        start = [float(c) for c in fin.readline().split()]
        sc = int(fin.readline())

        global func
        func = [fin.readline().split() for i in range(sc)]

        global ansFunc
        ansFunc = [fin.readline().split() for i in range(sc)]

        am = AdamsMethod(a, b, start)
        am.get_runge_kut_begin()

if __name__ == "__main__":
    main()