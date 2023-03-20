import math

import numpy as np
from matplotlib import pyplot as plt
from TestFunctions import *


class AdamsMethod:

    splits = 30

    def __init__(self, a, b, start):
        self.a = a
        self.b = b
        self.start = start
        self.step = abs(b - a) / self.splits

        self.system_count = len(start)
        self.dots = [[] for i in range(self.system_count)]

    def get_runge_kut_begin(self, func):
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
                tempF = eval(func[i])

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

    def adams_method(self, func):
        t = self.a

        by = self.get_runge_kut_begin(func)
        # print(*by, sep='\n')
        ly = [[] for i in range(5)]
        for i in range(5):
            for j in range(self.system_count):
                ly[i].append(by[j][i])

        last4Y, last3Y, last2Y, lastY, y = ly[0], ly[1], ly[2], ly[3], ly[4]
        last4F, last3F, last2F, lastF, f = ([] for i in range(5))
        for i in range(self.system_count):
            tempF = eval(func[i])
            last4F.append(tempF(t, last4Y))
            last3F.append(tempF(t + self.step, last3Y))
            last2F.append(tempF(t + self.step * 2, last2Y))
            lastF.append(tempF(t + self.step * 3, lastY))
            f.append(tempF(t + self.step * 4, y))

        newY = []
        newF = []

        t += self.step * 5
        while t <= self.b:
            for i in range(self.system_count):
                ny = y[i] + (self.step / 720) * \
                     (1901 * f[i] - 2774 * lastF[i] + 2616 * last2F[i] - 1274 * last3F[i] + 251 * last4F[i])
                newY.append(ny)
                self.dots[i].append((t, ny))

            for i in range(self.system_count):
                tempF = eval(func[i])
                newF.append(tempF(t, newY))

            f, lastF, last2F, last3F, last4F = newF, f, lastF, last2F, last3F
            y, lastY, last2Y, last3Y, last4Y = newY, y, lastY, last2Y, last3Y

            t += self.step
            newY = []
            newF = []

        return self.dots[0]
        # self.draw()