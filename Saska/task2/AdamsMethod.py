import math

import matplotlib.pyplot as plt
import numpy as np


func = None
ansFunc = None


# Test 1
def func1(x, y):
    return 2 * x - 3 + y


def ansFunc1(x):
    return math.e**x + 1 - 2 * x


# Test 2
def func2(x, y):
    return 4 / (x**2) - y**2 - y / x


def ansFunc2(x):
    return 2 / x + 4 / (x**5 - x)


# Test 3
def func3(x, y):
    return y / x + x * math.cos(x)


def ansFunc3(x):
    return x * math.sin(x)

# ----------------------------------------------------------------------------------------------------------------------


class AdamsMethod:

    splits = 50

    def __init__(self, a, b, y0):
        self.a = a
        self.b = b
        self.y0 = y0
        self.step = abs(b - a) / self.splits
        self.dots = []

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set(xlabel='Ось абсцисс', ylabel='Ось ординат', title='Метод Адамса 5-шаговый')
        self.ax.grid(True)

    def get_runge_kut_begin(self):
        begin_y = []

        h = 0.16
        # h = 0.06
        # h = 0.23
        y = self.y0
        x = self.a

        begin_y.append(y)
        self.dots.append((x, y))
        while len(begin_y) < 5:
            x += self.step

            k1 = func(x, y)
            k2 = func(x + 0.5 * h, y + 0.5 * h * k1)
            k3 = func(x + 0.5 * h, y + 0.5 * h * k2)
            k4 = func(x + h, y + h * k3)

            y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            begin_y.append(y)
            self.dots.append((x, y))

        return begin_y

    def adams_method(self):
        x = self.a

        last4Y, last3Y, last2Y, lastY, y = tuple(self.get_runge_kut_begin())
        last4F, last3F, last2F, lastF, f = \
            func(x, last4Y), func(x + self.step, last3Y), func(x + self.step * 2, last2Y), func(x + self.step * 3, lastY), func(x + self.step * 4, y)

        x += self.step * 5
        while x <= self.b:
            newY = y + (self.step / 720) * (1901 * f - 2774 * lastF + 2616 * last2F - 1274 * last3F + 251 * last4F)
            f, lastF, last2F, last3F, last4F = func(x, newY), f, lastF, last2F, last3F
            y, lastY, last2Y, last3Y, last4Y = newY, y, lastY, last2Y, last3Y

            self.dots.append((x, y))

            x += self.step

        print(*self.dots, sep='\n')

        xi = []
        yi = []
        for x, y in self.dots:
            xi.append(x)
            yi.append(y)

        self.ax.plot(tuple(xi), tuple(yi), color='indigo', linestyle='-', label='Полученная интерполяция')

        ansXi = []
        ansYi = []
        for x in np.arange(self.a, self.b+0.1, self.step):
            ansXi.append(x)
            ansYi.append(ansFunc(x))

        self.ax.plot(tuple(ansXi), tuple(ansYi), label='Точное решение')

        self.ax.scatter(tuple(ansXi), tuple(ansYi), color='black', label='Точки разбиения', s=15)

        self.ax.plot([], [], linestyle='', label=f'Невязка:{self.get_discrepancy(xi, yi, ansXi, ansYi)}')

        self.show_graphic()
        # return self.dots

    def get_discrepancy(self, dots1X, dots1Y, dots2X, dots2Y):
        dicr = 0
        for i in range(len(dots1X)):
            dot1 = (dots1X[i], dots1Y[i])
            dot2 = (dots2X[i], dots2Y[i])
            dist = math.sqrt((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)
            dicr += dist

        dicr /= len(dots1X)
        return dicr

    def show_graphic(self):
        self.ax.legend()
        plt.show()


def main():
    with open("input1.txt") as fin:
        a, b = map(float, fin.readline().split())
        y0 = float(fin.readline())

        global func
        func = eval(fin.readline().strip())

        global ansFunc
        ansFunc = eval(fin.readline().strip())

        method = AdamsMethod(a, b, y0)
        method.adams_method()


if __name__ == "__main__":
    main()