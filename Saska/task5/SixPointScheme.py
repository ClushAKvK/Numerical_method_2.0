import numpy as np
from matplotlib import pyplot as plt

from TestFunction import *


start = None
border = None
ans_func = None


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


class SixPointSchemeMethod:

    t_splits = 25
    x_splits = 20

    def __init__(self, alpha, l, T, f):
        self.func = f
        self.alpha = alpha
        self.l = l
        self.T = T
        self.x_step = l / self.x_splits
        self.t_step = T / self.t_splits

        self.dots = []

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set(xlabel='Ось абсцисс', ylabel='Ось ординат', title='6-точечная чисто неявная схема')
        self.ax.grid(True)

    def run(self):
        border1, border2 = (eval(border[0]), eval(border[1]))

        layer = [[] for i in range(self.t_splits)]

        x = 0
        # layer[0].append(border1(0))
        for i in range(self.x_splits + 1):
            layer[0].append(start(x))
            x += self.x_step
        # layer[0].append(border2(self.l))

        sigma = (self.alpha * self.t_step) / (2 * self.x_step**2)

        for i in range(1, self.t_splits):
            x = 0
            a, b, c, d = [None], [1], [0], [border1(0)]
            for j in range(1, self.x_splits):
                a.append(-sigma)
                b.append(2 * sigma + 1)
                c.append(-sigma)
                d.append(
                    sigma * layer[i - 1][j + 1] + (-2 * sigma + 1) * layer[i - 1][j] + sigma * layer[i - 1][j - 1] + self.func(x) * self.t_step
                )
                x += self.x_step

            a.append(0)
            b.append(1)
            c.append(None)
            d.append(border2(self.l))

            # layer[i].append(border1(0))
            layer[i].extend(sweep_method(a, b, c, d))
            # layer[i].append(border2(self.l))

        x = 0
        for i in range(0, len(layer[-1])):
            self.dots.append((x, layer[-1][i]))
            x += self.x_step

        # for la in layer:
        #     x = 0
        #     xi = []
        #     yi = []
        #     for i in la:
        #         xi.append(x)
        #         yi.append(i)
        #         x += self.x_step
        #     self.ax.plot(tuple(xi), tuple(yi), color='indigo', linestyle='-')
        #
        # self.ax.legend()
        # plt.show()
        #

        self.show_graphic()

    def show_graphic(self):
        xi = []
        yi = []
        for x, y in self.dots:
            xi.append(x)
            yi.append(y)

        self.ax.plot(tuple(xi), tuple(yi), color='indigo', linestyle='-', label='Численное решение')

        ansXi = []
        ansYi = []
        for x in np.arange(0, self.l + 0.001, self.x_step):
            ansXi.append(x)
            ansYi.append(ans_func(self.T, x))

        self.ax.plot(tuple(ansXi), tuple(ansYi), label='Точное решение')

        self.ax.scatter(tuple(xi), tuple(yi), color='black', label='Узлы', s=15)

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
            if maxDiscr < dist and dot1[0] < self.l and dot2[0] < self.l:
                maxDiscr = dist

        # dicr /= len(dots1X)
        # return dicr
        return maxDiscr


def main():
    with open('input1.txt') as fin:
        thermal_conductivity, l, T = map(float, fin.readline().split())

        f = eval(fin.readline().strip())

        global start
        start = eval(fin.readline().strip())

        global border
        border = [fin.readline().strip() for i in range(2)]

        global ans_func
        ans_func = eval(fin.readline().strip())

        method = SixPointSchemeMethod(thermal_conductivity, l, T, f)
        method.run()


if __name__ == '__main__':
    main()