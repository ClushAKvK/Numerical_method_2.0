import math


def funcY(t, params):
    return params[1]


# ----------------------------------------------------------------------------------------------------------------------


def funcZ(t, params):
    return -params[0] - t


def func1Z(t, params):
    return -t - params[0]


def ansFunc1Z(t):
    return math.sin(t) / math.sin(1) - t


def func2Z(t, params):
    return 8 + 5 * params[1] - 4 * params[0]


def ansFunc2Z(t):
    return 2 - 3/2 * math.e**t + 1/2 * math.e**(4 * t)


def func3Z(t, params):
    return 2 * t + params[0]


def ansFunc3Z(t):
    return math.e**(t + 1) / (math.e**2 - 1) - math.e**(-t + 1) / (math.e**2 - 1) - 2 * t

