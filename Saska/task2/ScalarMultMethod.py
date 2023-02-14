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


def scalar_mult_method(matrix, approx, eps):
    e = getNewApproximation(approx)
    approx = matrix.mult_by_vector(e)
    lmd = scalarMult(approx, e)
    lastLmd = lmd + 1
    e = getNewApproximation(approx)

    while abs(lmd - lastLmd) > eps:
        approx = matrix.mult_by_vector(e)
        lastLmd = lmd
        lmd = scalarMult(approx, e)
        e = getNewApproximation(approx)

    print('asdadasd a')

    return lmd


def main():
    with open('input4.txt', 'r') as fin:
        eps = 0.1**6
        approx = [float(x) for x in fin.readline().split()]
        matrix = []
        for line in fin:
            matrix.append(
                [float(x) for x in line.split()]
            )

    answer = scalar_mult_method(Matrix(matrix), approx, eps)
    print(answer)

    with open('output.txt', 'w') as fout:
        fout.write(answer.__str__())


if __name__ == "__main__":
    main()