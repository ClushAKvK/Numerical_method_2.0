import math

import matplotlib.pyplot as plt
import numpy as np
# from TestFunctions import *

func = None
ansFunc = None


# Test 1
# input
def func1X(t, params):
    """x' = x + z - y"""
    return params[0] + params[2] - params[1]


def func1Y(t, params):
    """y' = x + y - z"""
    return params[0] + params[1] - params[2]


def func1Z(t, params):
    """z' = 2 * x - y"""
    return 2 * params[0] - params[1]


# ans funcs
def ansFunc1X(t):
    return math.e**t + math.e**(2*t) + math.e**(-t)


def ansFunc1Y(t):
    return math.e**t - 3 * math.e**(-t)


def ansFunc1Z(t):
    return math.e**t + math.e**(2*t) - 5 * math.e**(-t)


#  Test 2

# input
def func2X(t, params):
    """x' = y + 2 * e^t"""
    return params[1] + 2 * math.e**t


def func2Y(t, params):
    """y' = x + t^2"""
    return params[0] + t**2


# ans funcs
def ansFunc2X(t):
    """x = e^t + e^(-t) + t * e^t - t^2 - 2"""
    return math.e**t + math.e**(-t) + t * math.e**t - t**2 - 2


def ansFunc2Y(t):
    """y = e^t - e^(-t) + (t - 1) * e^t - 2 * t"""
    return math.e**t - math.e**(-t) + (t - 1) * math.e**t - 2 * t


#  Test 3

# input
def func3X(t, params):
    """x' = t / y"""
    return t / params[1]


def func3Y(t, params):
    """y' = -(t / x)"""
    return -1 * (t / params[0])


# ans funcs
def ansFunc3X(t):
    """x = e^(t^2)"""
    return math.e**(t**2)


def ansFunc3Y(t):
    """y = 1/2 * e^(-t^2)"""
    return 0.5 * math.e**(-1 * (t**2))


#  Test 3

# input
def func4X(t, params):
    """2 * y * x' = x^2 - y^2 + 1"""
    return params[0]**2 / (2 * params[1]) - params[1] / 2 + 1 / (2 * params[1])


def func4Y(t, params):
    """y' = y + x"""
    return params[1] + params[0]


# ans funcs
def ansFunc4X(t):
    """x = e^(t^2)"""
    return 1 / 2 * t - 1 / 4 * t**2 - 1


def ansFunc4Y(t):
    """y = 1/2 * e^(-t^2)"""
    return 1 + 1 / 4 * t**2


class RungeKutMethod:

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

    def run(self):

        h = self.step
        y = self.start
        newY = []
        t = self.a

        for i in range(self.system_count):
            self.dots[i].append((t, y[i]))

        while t <= self.b + 0.001:
            # print(t)
            t += self.step

            for i in range(self.system_count):
                tempF = eval(*func[i])

                k1 = h * tempF(t, y)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + k1)
                k2 = h * tempF(t + h, params)

                ny = y[i] + 0.5 * (k1 + k2)

                newY.append(ny)
                self.dots[i].append((t, ny))

            y = newY
            newY = []

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

    with open('input3.txt') as fin:
        a, b = map(float, fin.readline().split())
        start = [float(c) for c in fin.readline().split()]
        sc = int(fin.readline())

        global func
        func = [fin.readline().split() for i in range(sc)]

        global ansFunc
        ansFunc = [fin.readline().split() for i in range(sc)]

        rk = RungeKutMethod(a, b, start)
        rk.run()


if __name__ == "__main__":
    main()
