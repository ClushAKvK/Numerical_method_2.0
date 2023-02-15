import math

import numpy as np


class Matrix:

    def __init__(self, matrix):
        self.__matrix = matrix
        self.rows = len(matrix)
        self.columns = len(matrix[0])

    def get(self, i, j):
        return self.__matrix[i][j]

    def mult_by_vector(self, vector):
        result = np.array(vector, float)
        result.fill(0)
        for i in range(self.rows):
            for j in range(self.columns):
                result[i] += self.__matrix[i][j] * vector[j]
        return list(result)


def norm(vector):
    return math.sqrt(sum(x * x for x in vector))


def scalarMult(vec1, vec2):
    return sum(x * y for x, y in zip(vec1, vec2))


def getNewApproximation(vec):
    n = norm(vec)
    return [x / n for x in vec]


def power_method(matrix, approx, eps):
    y = matrix.mult_by_vector(approx)
    lmd = scalarMult(y, approx)
    lastLmd = lmd + 1
    approx = getNewApproximation(y)
    while abs(lmd - lastLmd) > eps:
        y = matrix.mult_by_vector(approx)
        lastLmd = lmd
        lmd = scalarMult(y, approx)
        approx = getNewApproximation(y)
    return (lmd, approx)


def main():
    with open('input1.txt', 'r') as fin:
        eps = 0.1**6
        approx = [float(x) for x in fin.readline().split()]
        matrix = []
        for line in fin:
            matrix.append(
                [float(x) for x in line.split()]
            )

    answer, vec = power_method(Matrix(matrix), approx, eps)
    print(answer)
    print(vec)

    with open('output.txt', 'w') as fout:
        fout.write(answer.__str__())


if __name__ == "__main__":
    main()