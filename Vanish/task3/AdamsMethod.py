import matplotlib.pyplot as plt
import numpy as np
from TestFunctions import *

func = None
ansFunc = None


class HalfDivision:
    eps = 0.1**5

    n = 50

    def run(self, left, right, x, lastY, h, func):
        y = []
        for i in range(self.n):
            a = left + i * (right - left) / self.n
            b = left + (i + 1) * (right - left) / self.n

            check_a = a - h * func(x, a) - lastY
            check_b = b - h * func(x, b) - lastY

            if check_a * check_b < 0:
                y.append(self.method(a, b, x, lastY, h, func))

        minY = y.pop()
        for i in y:
            if abs(i - lastY) < abs(minY - lastY):
                minY = i

        return minY

    def method(self, left, right, x, lastY, h, func):

        while abs(right - left) > self.eps:
            c = (left + right) / 2
            # temp = func(right, c)
            check_left = left - h * func(x, left) - lastY
            check_c = c - h * func(x, c) - lastY
            if check_left * check_c < 0:
                right = c
            else:
                left = c

        return (left + right) / 2


class AdamsMethod:

    splits = 30

    def __init__(self, a, b, start):
        self.a = a
        self.b = b
        self.start = start
        self.step = abs(b - a) / self.splits

        self.system_count = len(start)
        self.dots = [[] for i in range(self.system_count)]

        self.fig, self.axs = plt.subplots(1, self.system_count, figsize=(20, 5))
        for i in range(self.system_count):
            tempF = eval(*func[i])
            self.axs[i].set(xlabel='Ось абсцисс', ylabel='Ось ординат', title=tempF.__doc__)
            self.axs[i].grid(True)


    def eiler(self):
        h = self.step
        y = self.start
        t = self.a

        for i in range(self.system_count):
            self.dots[i].append((t, y[i]))

        hd = HalfDivision()
        while t < self.b:
            t += self.step
            for i in range(self.system_count):
                temp_func = eval(*func[i])
                y[i] = hd.run(y[i] - 100, y[i] + 100, t, y[i], h, temp_func)
                self.dots[i].append((t, y[i]))

        self.draw()

    def get_discrepancy(self, dots1X, dots1Y, dots2X, dots2Y):
        # dicr = 0
        maxDiscr = -1
        for i in range(min(len(dots1X), len(dots2X))):
            dot1 = (dots1X[i], dots1Y[i])
            dot2 = (dots2X[i], dots2Y[i])
            dist = math.sqrt((dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2)
            # dicr += dist
            if maxDiscr < dist and dot1[0] < self.b and dot2[0] < self.b:
                maxDiscr = dist

        # dicr /= len(dots1X)
        # return dicr
        return maxDiscr

    def draw(self):
        xi = [[] for i in range(self.system_count)]
        yi = [[] for i in range(self.system_count)]
        for i in range(self.system_count):
            for x, y in self.dots[i]:
                # if x <= self.b:
                xi[i].append(x)
                yi[i].append(y)

        ansXi = [[] for i in range(self.system_count)]
        ansYi = [[] for i in range(self.system_count)]
        for i in range(self.system_count):
            tempF = eval(*ansFunc[i])
            for t in np.arange(self.a, self.b + 0.1, self.step):
                # if t <= self.b:
                ansXi[i].append(t)
                ansYi[i].append(tempF(t))

        for i in range(self.system_count):
            self.axs[i].plot(tuple(xi[i]), tuple(yi[i]), color='indigo', linestyle='-', label='Полученная интерполяция')
            self.axs[i].plot(tuple(ansXi[i]), tuple(ansYi[i]), label='Точное решение')
            self.axs[i].scatter(tuple(ansXi[i]), tuple(ansYi[i]), color='black', label='Точки разбиения', s=15)
            self.axs[i].plot([], [], linestyle='', label=f'Погрешность:{self.get_discrepancy(xi[i], yi[i], ansXi[i], ansYi[i])}')
            self.axs[i].legend()

        plt.show()


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
        am.eiler()


if __name__ == "__main__":
    main()