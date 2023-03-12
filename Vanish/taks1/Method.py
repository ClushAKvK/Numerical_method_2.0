import math
import random

import numpy as np


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

        if temp == 0:
            idx = -1
            for p in range(k + 1, n):
                if A[p][k] != 0:
                    idx = p

            for p in range(len(A[k])):
                temp = A[k][p]
                A[k][p] = A[idx][p]
                A[idx][p] = temp

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


def foo(tempY, lastX):
    temp = []
    for y, x in zip(tempY, lastX):
        if x != 0:
            temp.append(y / x)

    return temp[len(temp) // 2]
    sum_ = sum(temp)
    # return sum_ / len(temp)
    # random_index = random.randint(0, len(temp) - 1)
    # return temp[random_index]


def make_result(matrix, y0):
    global eps
    matrix = inversion(matrix, len(matrix))

    normY = norm(y0)
    lastX = [i / normY for i in y0]
    y = multiplyMatrixByVector(matrix, lastX)

    lmd = foo(y, lastX)
    lastLmd = lmd + 1

    while abs(lmd - lastLmd) > eps:
        normY = norm(y)
        lastX = [i / normY for i in y]
        y = multiplyMatrixByVector(matrix, lastX)
        lastLmd = lmd
        lmd = foo(y, lastX)

    normY = norm(y)
    x = [i / normY for i in y]
    return (1 / lmd, x)


eps = 0.1**6

fin = open('input1.txt', 'r')

start = [float(x) for x in fin.readline().split()]
matr = []
for line in fin:
    matr.append([float(x) for x in line.split()])


ownLmd, ownVec = make_result(matr, start)

print(ownLmd)
print(ownVec)

# print(answer)

fin.close()