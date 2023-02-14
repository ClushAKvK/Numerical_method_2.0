import math

import numpy as np


def mult_matr_on_vec(matrix, vector):
    rows = len(matrix)
    columns = len(matrix[0])
    result = np.array(vector, float)
    result.fill(0)
    for i in range(rows):
        for j in range(columns):
            result[i] += matrix[i][j] * vector[j]
    return list(result)


def norm(vector):
    maxEl = vector[0]
    for el in vector:
        if abs(maxEl) < abs(el):
            maxEl = el
    return maxEl
    # return math.sqrt(sum(x * x for x in vector))

def scalar(vec1, vec2):
    ans = 0
    for i in range(len(vec1)):
        ans += vec1[i] * vec2[i]
    return ans


def make_result(matrix, start):
    global eps
    y = mult_matr_on_vec(matrix, start)
    temp = scalar(y, start)
    lastTemp = temp + 1

    n = norm(y)
    start = []
    for i in y: start.append(i / n)

    while abs(temp - lastTemp) > eps:
        y = mult_matr_on_vec(matrix, start)
        lastTemp = temp
        temp = scalar(y, start)
        n = norm(y)
        start = []
        for i in y: start.append(i / n)

    return temp


eps = 0.1**6

fin = open('input3.txt', 'r')

start = [float(x) for x in fin.readline().split()]
matr = []
for line in fin:
    matr.append([float(x) for x in line.split()])

answer = make_result(matr, start)
print(answer)

fin.close()