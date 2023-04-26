import numpy as np
import random
from matplotlib import pyplot as plt

from TestFunctions import *
from RungeKut import *

func = None
ansFunc = None


class Method:

    eps = 0.1**5

    def __init__(self, a, b, A, B):
        self.a = a
        self.b = b
        self.A = A
        self.B = B
        self.dots = []

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set(xlabel='Ось абсцисс', ylabel='Ось ординат', title='Метод стрельбы')
        self.ax.grid(True)

    def shooting_method(self):

        last_n = random.random() * 10
        # last_n = -100
        rk = RungeKut(self.a, self.b, [self.A, last_n])
        last_y = rk.method(func)

        # n = 100
        n = random.random() * 100
        rk = RungeKut(self.a, self.b, [self.A, n])
        y = rk.method(func)
        while (self.get_b_el(last_y)[1] - self.b) * (self.get_b_el(y)[1] - self.b) > 0:
            n = random.random() * 100 * (-1)**int(n)
            rk = RungeKut(self.a, self.b, [self.A, n])
            y = rk.method(func)
            # print(n)

        # print(self.get_b_el(last_y)[1])
        # print(self.get_b_el(y)[1])

        mid_n = (n + last_n) / 2
        rk = RungeKut(self.a, self.b, [self.A, mid_n])
        mid_y = rk.method(func)

        while abs(self.get_b_el(mid_y)[1] - self.B) > self.eps:
            if (self.get_b_el(mid_y)[1] - self.B) * (self.get_b_el(last_y)[1] - self.B) <= 0:
                n = mid_n
                y = mid_y
            else:
                last_n = mid_n
                last_y = mid_y

            mid_n = (n + last_n) / 2
            rk = RungeKut(self.a, self.b, [self.A, mid_n])
            mid_y = rk.method(func)

        self.dots = mid_y
        self.show_graphic()

    def get_b_el(self, ys):
        close_el = (self.a, self.a)
        for i, el in enumerate(ys):
            if abs(el[0] - self.b) < abs(close_el[0] - self.b):
                close_el = el
        return close_el

    def show_graphic(self):
        xi = []
        yi = []
        for x, y in self.dots:
            xi.append(x)
            yi.append(y)

        self.ax.plot(tuple(xi), tuple(yi), color='indigo', linestyle='-', label='Численное решение')

        ansXi = []
        ansYi = []
        for x in np.arange(self.a, self.b + 0.001, (self.b - self.a) / len(xi)):
            ansXi.append(x)
            ansYi.append(ansFunc(x))

        self.ax.plot(tuple(ansXi), tuple(ansYi), label='Точное решение')

        self.ax.scatter(tuple(ansXi), tuple(ansYi), color='black', label='Точки разбиения', s=15)

        self.ax.plot([], [], linestyle='', label=f'Погрешность:{self.get_discrepancy(xi, yi, ansXi, ansYi)}')

        self.ax.legend()
        plt.show()

    def get_discrepancy(self, dots1X, dots1Y, dots2X, dots2Y):
        # dicr = 0
        maxDiscr = -1
        for i in range(len(dots1X) - 1):
            dot1 = (dots1X[i], dots1Y[i])
            dot2 = (dots2X[i], dots2Y[i])
            dist = math.sqrt((dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2)
            # dicr += dist
            if maxDiscr < dist and dot1[0] < self.b and dot2[0] < self.b:
                maxDiscr = dist

        # dicr /= len(dots1X)
        # return dicr
        return maxDiscr


def main():
    with open('input1.txt') as fin:
        a, b = map(float, fin.readline().split())
        A, B = map(float, fin.readline().split())

        global func
        func = ['funcY', fin.readline().strip()]

        global ansFunc
        ansFunc = eval(fin.readline().strip())

        sm = Method(a, b, A, B)
        sm.shooting_method()


if __name__ == '__main__':
    main()