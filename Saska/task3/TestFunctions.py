import math


# Test 1

# input
def func1X(t, params):
    # x' = x + z - y
    return params[0] + params[2] - params[1]


def func1Y(t, params):
    # y' = x + y - z
    return params[0] + params[1] - params[2]


def func1Z(t, params):
    # z' = 2 * x - y
    return 2 * params[0] - params[1]


# ans funcs
def ansFunc1X(t):
    return math.e**t + math.e**(2*t) + math.e**(-t)


def ansFunc1Y(t):
    return math.e**t - 3 * math.e**(-t)


def ansFunc1Z(t):
    return math.e**t + math.e**(2*t) - 5 * math.e**(-t)


#  TEst 2