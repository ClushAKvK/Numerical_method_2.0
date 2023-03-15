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


# class Newton:
#     eps = 0.1**5
#
#     def difference_Newton(self, right, eps):
#         x = right
#         lastX = x - 1
#         h = 0.1
#
#         while abs(func(lastX) - func(x)) < eps:
#             lastX = x
#             temp = (func(x) * h) / (func(x + h) - func(x))
#             x -= temp
#             h /= 10
#
#         return x


class HalfDivision:
    eps = 0.1**5

    n = 50

    def run(self, left, right, x, lastY, h):
        y = []
        for i in range(self.n):
            a = left + i * (right - left) / self.n
            b = left + (i + 1) * (right - left) / self.n

            check_a = a - h * func(x, a) - lastY
            check_b = b - h * func(x, b) - lastY

            if check_a * check_b < 0:
                y.append(self.method(a, b, x, lastY, h))

        minY = y.pop()
        for i in y:
            if abs(i - lastY) < abs(minY - lastY):
                minY = i

        return minY

    def method(self, left, right, x, lastY, h):

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


class EilerMethod:

    splits = 30

    def __init__(self, a, b, y0):
        self.a = a
        self.b = b
        self.y0 = y0
        self.step = abs(b - a) / self.splits
        self.dots = []

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set(xlabel='Ось абсцисс', ylabel='Ось ординат', title='Метод Эйлера')
        self.ax.grid(True)

    def eiler(self):
        h = self.step
        y = self.y0
        x = self.a

        self.dots.append((x, y))
        # while x < self.b:
        #     x += self.step
        #     y = y + h * func(x, y)
        #     self.dots.append((x, y))

        hd = HalfDivision()
        lastY = y - 1
        while x < self.b:
            x += self.step
            y = hd.run(y - 100, y + 100, x, y, h)
            self.dots.append((x, y))

        xi = []
        yi = []
        for x, y in self.dots:
            xi.append(x)
            yi.append(y)

        self.ax.plot(tuple(xi), tuple(yi), color='indigo', linestyle='-', label='Полученная интерполяция')

        ansXi = []
        ansYi = []
        for x in np.arange(self.a, self.b + 0.1, self.step):
            ansXi.append(x)
            ansYi.append(ansFunc(x))

        self.ax.plot(tuple(ansXi), tuple(ansYi), label='Точное решение')

        self.ax.scatter(tuple(ansXi), tuple(ansYi), color='black', label='Точки разбиения', s=15)

        self.ax.plot([], [], linestyle='', label=f'Погрешность:{self.get_discrepancy(xi, yi, ansXi, ansYi)}')

        self.show_graphic()

    def get_discrepancy(self, dots1X, dots1Y, dots2X, dots2Y):
        maxDiscr = -1
        for i in range(len(dots1X)):
            if dots1X[i] <= self.b and dots2X[i] <= self.b:
                dot1 = (dots1X[i], dots1Y[i])
                dot2 = (dots2X[i], dots2Y[i])
                dist = math.sqrt((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)
                # dicr += dist
                if maxDiscr < dist:
                    maxDiscr = dist
        return maxDiscr

    def show_graphic(self):
        self.ax.legend()
        plt.show()


def main():
    with open("input2.txt") as fin:
        a, b = map(float, fin.readline().split())
        y0 = float(fin.readline())

        global func
        func = eval(fin.readline().strip())

        global ansFunc
        ansFunc = eval(fin.readline().strip())

        method = EilerMethod(a, b, y0)
        method.eiler()


if __name__ == "__main__":
    main()