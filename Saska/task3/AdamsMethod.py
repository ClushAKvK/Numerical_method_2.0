import matplotlib.pyplot as plt
import numpy as np
from TestFunctions import *

func = None
ansFunc = None


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

                # RANK 5
                k1 = 1/3 * h * tempF(t, y)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + k1)
                k2 = 1/3 * h * tempF(t + 1/3 * h, params)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + 1/2 * k1 + 1/2 * k2)
                k3 = 1/3 * h * tempF(t + 1/3 * h, params)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + 3/8 * k1 + 9/8 * k3)
                k4 = 1/3 * h * tempF(t + 1/2 * h, params)

                params = []
                for j in range(self.system_count):
                    params.append(y[j] + 3/2 * k1 - 9/2 * k3 + 6 * k4)
                k5 = 1 / 3 * h * tempF(t + h, params)

                ny = y[i] + 1/2 * (k1 + 4 * k4 + k5)


                # Rank 4
                # k1 = tempF(t, y)
                #
                # params = []
                # for j in range(self.system_count):
                #     params.append(y[j] + 0.5 * h * k1)
                # k2 = tempF(t + 0.5 * h, params)
                #
                # params = []
                # for j in range(self.system_count):
                #     params.append(y[j] + 0.5 * h * k2)
                # k3 = tempF(t + 0.5 * h, params)
                #
                # params = []
                # for j in range(self.system_count):
                #     params.append(y[j] + h * k3)
                # k4 = tempF(t + h, params)
                #
                # # ~~~
                # ny = y[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

                newY.append(ny)
                begin_y[i].append(ny)
                self.dots[i].append((t, ny))

            y = newY
            newY = []

        # print(*self.dots, sep='\n')
        # print(*begin_y, sep='\n')
        return begin_y

    def adams_method(self):
        t = self.a

        by = self.get_runge_kut_begin()
        print(*by, sep='\n')
        ly = [[] for i in range(5)]
        for i in range(5):
            for j in range(self.system_count):
                ly[i].append(by[j][i])

        last4Y, last3Y, last2Y, lastY, y = ly[0], ly[1], ly[2], ly[3], ly[4]
        last4F, last3F, last2F, lastF, f = ([] for i in range(5))
        for i in range(self.system_count):
            tempF = eval(*func[i])
            last4F.append(tempF(t, last4Y))
            last3F.append(tempF(t + self.step, last3Y))
            last2F.append(tempF(t + self.step * 2, last2Y))
            lastF.append(tempF(t + self.step * 3, lastY))
            f.append(tempF(t + self.step * 4, y))

        newY = []
        newF = []

        t += self.step * 5
        while t <= self.b + 0.1:
            for i in range(self.system_count):
                ny = y[i] + (self.step / 720) * \
                     (1901 * f[i] - 2774 * lastF[i] + 2616 * last2F[i] - 1274 * last3F[i] + 251 * last4F[i])
                newY.append(ny)
                self.dots[i].append((t, ny))

            for i in range(self.system_count):
                tempF = eval(*func[i])
                newF.append(tempF(t, newY))

            f, lastF, last2F, last3F, last4F = newF, f, lastF, last2F, last3F
            y, lastY, last2Y, last3Y, last4Y = newY, y, lastY, last2Y, last3Y

            t += self.step
            newY = []
            newF = []

        self.draw()

    def get_discrepancy(self, dots1X, dots1Y, dots2X, dots2Y):
        # dicr = 0
        maxDiscr = -1
        for i in range(len(dots1X)):
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

    with open('input2.txt') as fin:
        a, b = map(float, fin.readline().split())
        start = [float(c) for c in fin.readline().split()]
        sc = int(fin.readline())

        global func
        func = [fin.readline().split() for i in range(sc)]

        global ansFunc
        ansFunc = [fin.readline().split() for i in range(sc)]

        am = AdamsMethod(a, b, start)
        am.adams_method()


if __name__ == "__main__":
    main()