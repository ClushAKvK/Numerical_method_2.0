import math

import numpy as np

from Vanish.task0.Method import make_results


def inversion(A, n):
    E = []
    for i in range(n):
        lineE = []
        for j in range(n):
            if i == j: lineE.append(1)
            else: lineE.append(0)
        E.append(lineE)

    for k in range(n):
        temp = A[k][k]

        for j in range(n):
            A[k][j] /= temp
            E[k][j] /= temp

        for i in range(k + 1, n):
            temp = A[i][k]

            for j in range(n):
                A[i][j] -= A[k][j] * temp
                E[i][j] -= E[k][j] * temp

    for k in range(n - 1, 0, -1):
        for i in range(k - 1, -1, -1):
            temp = A[i][k]
            for j in range(n):
                A[i][j] -= A[k][j] * temp
                E[i][j] -= E[k][j] * temp

    return E


def multiplyMatrixByVector(matrix, vector):
    rows = len(matrix)
    columns = len(matrix[0])
    result = np.array(vector, float)
    result.fill(0)
    for i in range(rows):
        for j in range(columns):
            result[i] += matrix[i][j] * vector[j]
    return list(result)


def norm(vector):
    return math.sqrt(sum(x * x for x in vector))


def scalar(vec1, vec2):
    ans = 0
    for i in range(len(vec1)):
        ans += vec1[i] * vec2[i]
    return ans


def transpose_matrix(matrix):
    result = []
    temp = zip(*matrix)
    for line in temp:
        result.append(list(line))
    return result


def multiplyMatricesCell(firstMatrix, secondMatrix, row, col):
    cell = 0
    for i in range(len(secondMatrix)):
        cell += firstMatrix[row][i] * secondMatrix[i][col]
    return cell


def multiplyMatrices(firstMatrix, secondMatrix):
    result = []

    for row in range(len(firstMatrix)):
        temp = []
        for col in range(len(secondMatrix[0])):
            temp.append(multiplyMatricesCell(firstMatrix, secondMatrix, row, col))
        result.append(temp)
    return result


def getNewApproximation(vec):
    n = norm(vec)
    return [x / n for x in vec]


def getLamda(y, lastX):
    lmd = []
    for i in range(len(y)):
        if lastX[i] != 0:
            lmd.append(y[i] / lastX[i])
    ans = sum(lmd) / len(lmd)
    return ans


def make_result(matrix, start):
    global eps

    matrix = inversion(matrix, len(matrix))

    lastX = getNewApproximation(start)
    lastY = multiplyMatrixByVector(matrix, start)
    lastLmd = getLamda(lastY, start)

    x = getNewApproximation(lastY)
    y = multiplyMatrixByVector(matrix, lastY)
    lmd = getLamda(y, lastX)

    while abs(lmd - lastLmd) > eps:
        lastX = x
        lastY = y
        lastLmd = lmd

        x = getNewApproximation(lastY)
        y = multiplyMatrixByVector(matrix, lastY)
        lmd = getLamda(y, lastX)

    return (1/lmd, getNewApproximation(y))


eps = 0.1**6

fin = open('input2.txt', 'r')

start = [float(x) for x in fin.readline().split()]
matr = []
for line in fin:
    matr.append([float(x) for x in line.split()])


ownLmd, ownVec = make_results(matr, start)

print(ownLmd)
print(ownVec)

# print(answer)

fin.close()