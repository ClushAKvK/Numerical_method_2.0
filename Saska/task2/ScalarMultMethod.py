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


def getTempX2Vector(x0, x1, x2):
    tempX2 = []
    for i in range(len(x0)):
        tempX2.append(
            (x0[i] * x2[i] - x1[i]**2) / (x2[i] - 2 * x1[i] + x0[i])
        )
    return tempX2


def scalar_mult_method(matrix, x0, eps):

    # Step 1-1
    e = getNewApproximation(x0)
    x1 = matrix.mult_by_vector(e)

    # Step 1-2
    e = getNewApproximation(x1)
    x2 = matrix.mult_by_vector(e)
    lmd2 = scalarMult(x2, e)

    # Step 2
    e = getNewApproximation(x2)
    tempX2 = getTempX2Vector(x0, x1, x2)
    tempLmd = scalarMult(tempX2, e)

    # Step 3
    e = getNewApproximation(tempX2)
    x3 = matrix.mult_by_vector(e)
    lmd3 = scalarMult(x3, e)

    # Step 4
    while abs(lmd3 - lmd2) > eps:
        x0 = tempX2
        x1 = x3

        e = getNewApproximation(x1)
        x2 = matrix.mult_by_vector(e)
        lmd2 = scalarMult(x2, e)

        e = getNewApproximation(x2)
        tempX2 = getTempX2Vector(x0, x1, x2)
        tempLmd = scalarMult(tempX2, e)

        # Step 3
        e = getNewApproximation(tempX2)
        x3 = matrix.mult_by_vector(e)
        lmd3 = scalarMult(x3, e)

    return lmd3


def main():
    with open('input1.txt', 'r') as fin:
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