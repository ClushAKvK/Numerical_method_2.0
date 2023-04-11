import math

import numpy as np
from matplotlib import pyplot as plt
from test_functions import *

px, fx = None, None
ansFunc = None


def simple_method(min_x, max_x, min_x0, max_x0):

    def sweep_method(a, b, c, d):
        # border1, border2 = (eval(border[0]), eval(border[1]))
        # p = [0]
        # q = [border1(0)]
        p = [None, -c[0] / b[0]]
        q = [None, d[0] / b[0]]

        # p.append(-c[0] / b[0])
        # q.append(d[0] / b[0])

        for i in range(1, len(d) - 1):
            p.append(-c[i] / (a[i] * p[i] + b[i]))
            q.append((d[i] - a[i] * q[i]) / (a[i] * p[i] + b[i]))

        # p.append(border2(1))
        # q.append(0)
        # p.append(-c[len(c) - 1])
        # q.append()

        m = len(a) - 1
        # lastX = border2(1)
        lastX = (d[m] - a[m] * q[m]) / (p[m] * a[m] + b[m])
        x = [lastX]
        while m != 0:
            m -= 1
            newX = lastX * p[m + 1] + q[m + 1]
            x.append(newX)
            lastX = newX

        # x.append(bo)
        # x[0] = border2(1)
        # print(x[::-1])

        return x[::-1]

    def get_discrepancy(dots1X, dots1Y, dots2X, dots2Y, a, b):
        # dicr = 0
        maxDiscr = -1
        for i in range(len(dots1X) - 1):
            dot1 = (dots1X[i], dots1Y[i])
            dot2 = (dots2X[i], dots2Y[i])
            dist = math.sqrt((dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2)
            # dicr += dist
            if maxDiscr < dist and dot1[0] < b and dot2[0] < b:
                maxDiscr = dist

        # dicr /= len(dots1X)
        # return dicr
        return maxDiscr

    def draw(dots, a, b):

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set(xlabel='Ось абсцисс', ylabel='Ось ординат', title='Метод стрельбы')
        ax.grid(True)

        xi = []
        yi = []
        for x, y in dots:
            xi.append(x)
            yi.append(y)

        ax.plot(tuple(xi), tuple(yi), color='indigo', linestyle='-', label='Численное решение')

        ansXi = []
        ansYi = []
        for x in np.arange(a, b + 0.001, (b - a) / len(xi)):
            ansXi.append(x)
            ansYi.append(ansFunc(x))

        # ax.plot(tuple(ansXi), tuple(ansYi), label='Точное решение')

        ax.scatter(tuple(xi), tuple(yi), color='black', label='Точки разбиения', s=15)

        ax.plot([], [], linestyle='', label=f'Погрешность:{get_discrepancy(xi, yi, ansXi, ansYi, a, b)}')

        ax.legend()
        plt.show()

    split = 50

    h = abs(max_x - min_x) / split

    dots = [(min_x, min_x0)]

    x = min_x + h
    a, b, c, d = [], [], [], []
    for i in range(split - 1):
        a.append(1)
        b.append(-(2 + h**2 * px(x)))
        c.append(1)
        d.append(h**2 * fx(x))
        x += h

    ys = sweep_method(a, b, c, d)

    x = min_x + h
    for y in ys:
        dots.append((x, y))
        x += h

    dots.append((max_x, max_x0))

    draw(dots, min_x, max_x)


def main():
    with open('input3.txt') as fin:
        min_x, max_x = map(float, fin.readline().split())
        min_x0, max_x0 = map(float, fin.readline().split())

        global px
        px = eval(fin.readline().strip())

        global fx
        fx = eval(fin.readline().strip())

        global ansFunc
        ansFunc = eval(fin.readline().strip())

        simple_method(min_x, max_x, min_x0, max_x0)


if __name__ == '__main__':
    main()