import matplotlib.pyplot as plt
import numpy as np
from TestFunctions import *

func = None
ansFunc = None


class HalfDivision:
    eps = 0.1**5

    n = 3

    def run(self, left, right, t, lastY, h):
        system_count = len(left)
        y = [[] for i in range(system_count)]

        # for i in range(self.n):
        #     a = []
        #     b = []
        #     for j in range(system_count):
        #         a.append(left[j] + i * (right[j] - left[j]) / self.n)
        #         b.append(left[j] + (i + 1) * (right[j] - left[j]) / self.n)
        #
        #     check_a = a[idx] - h * func(x, a) - lastY[idx]
        #     check_b = b[idx] - h * func(x, b) - lastY[idx]
        #
        #     if check_a * check_b < 0:
        #         y.append(self.method(a, b, x, lastY, h, func, idx))

        for i in range(self.n):
            b = []
            a = []
            for j in range(system_count):
                a.append(left[j] + i * (right[j] - left[j]) / self.n)
                b.append(left[j] + (i + 1) * (right[j] - left[j]) / self.n)

            for j in range(system_count):
                temp_func = eval(*func[j])
                check_a = a[j] - h * temp_func(t, a) - lastY[j]
                check_b = b[j] - h * temp_func(t, b) - lastY[j]

                if check_a * check_b < 0:
                    y[j].append(self.method(a, b, t, lastY, h, temp_func, j))

        new_Y = []
        for i in range(system_count):
            minY = y[i].pop()
            for j in y[i]:
                if abs(j - lastY[i]) < abs(minY - lastY[i]):
                    minY = j
            new_Y.append(minY)

        # minY = y.pop()
        # for i in y:
        #     if abs(i - lastY[idx]) < abs(minY - lastY[idx]):
        #         minY = i

        return new_Y

    def method(self, left, right, x, lastY, h, func, idx):
        system_count = len(left)
        while abs(right[idx] - left[idx]) > self.eps:
            c = []
            for i in range(system_count):
                c.append((left[i] + right[i]) / 2)
            # temp = func(right, c)
            check_left = left[idx] - h * func(x, left) - lastY[idx]
            check_c = c[idx] - h * func(x, c) - lastY[idx]
            if check_left * check_c < 0:
                right = c
            else:
                left = c

        return (left[idx] + right[idx]) / 2

    # def method(self, lefts, rights, t, lastY, h, idx):
    #     system_count = len(lefts)
    #     while max([abs(right - left) for right, left in zip(rights, lefts)]) > self.eps:
    #         c = []
    #         for i in range(system_count):
    #             c.append((lefts[i] + rights[i]) / 2)
    #
    #         for i in range(system_count):
    #             temp_func = eval(*func[i])
    #             check_left = lefts[i] - h * temp_func(t, lefts) - lastY[i]
    #             check_c = c[i] - h * temp_func(t, c) - lastY[i]
    #             if check_left * check_c < 0:
    #                 rights[i] = c[i]
    #             else:
    #                 lefts[i] = c[i]

        # return [(left + right) / 2 for left, right in zip(lefts, rights)]
        # return (lefts[idx] + rights[idx]) / 2

class Eiler:

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
            ny = []
            left = [ys - 10000 for ys in y]
            right = [ys + 10000 for ys in y]
            y = hd.run(left, right, t, y, h)

            for i in range(self.system_count):
                self.dots[i].append((t, y[i]))
            # for i in range(self.system_count):
            #     temp_func = eval(*func[i])
            #     temp_y = hd.run(left, right, t, y, h, temp_func, i)
            #     ny.append(temp_y)
            #     self.dots[i].append((t, temp_y))
            # y = hd.run(left, right, x)
            # y = ny

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

    with open('input3.txt') as fin:
        a, b = map(float, fin.readline().split())
        start = [float(c) for c in fin.readline().split()]
        sc = int(fin.readline())

        global func
        func = [fin.readline().split() for i in range(sc)]

        global ansFunc
        ansFunc = [fin.readline().split() for i in range(sc)]

        ei = Eiler(a, b, start)
        ei.eiler()


if __name__ == "__main__":
    main()