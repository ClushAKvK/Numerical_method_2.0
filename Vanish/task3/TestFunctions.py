import math


# Test 1

# input
def func1X(t, params):
    """x' = x + z - y"""
    return params[0] + params[2] - params[1]


def func1Y(t, params):
    """y' = x + y - z"""
    return params[0] + params[1] - params[2]


def func1Z(t, params):
    """z' = 2 * x - y"""
    return 2 * params[0] - params[1]


# ans funcs
def ansFunc1X(t):
    return math.e**t + math.e**(2*t) + math.e**(-t)


def ansFunc1Y(t):
    return math.e**t - 3 * math.e**(-t)


def ansFunc1Z(t):
    return math.e**t + math.e**(2*t) - 5 * math.e**(-t)


#  Test 2

# input
def func2X(t, params):
    """x' = y + 2 * e^t"""
    return params[1] + 2 * math.e**t


def func2Y(t, params):
    """y' = x + t^2"""
    return params[0] + t**2


# ans funcs
def ansFunc2X(t):
    """x = e^t + e^(-t) + t * e^t - t^2 - 2"""
    return math.e**t + math.e**(-t) + t * math.e**t - t**2 - 2


def ansFunc2Y(t):
    """y = e^t - e^(-t) + (t - 1) * e^t - 2 * t"""
    return math.e**t - math.e**(-t) + (t - 1) * math.e**t - 2 * t


#  Test 3

# input
def func3X(t, params):
    """x' = t / y"""
    return t / params[1]


def func3Y(t, params):
    """y' = -(t / x)"""
    return -1 * (t / params[0])


# ans funcs
def ansFunc3X(t):
    """x = e^(t^2)"""
    return math.e**(t**2)


def ansFunc3Y(t):
    """y = 1/2 * e^(-t^2)"""
    return 0.5 * math.e**(-1 * (t**2))


#  Test 3

# input
def func4X(t, params):
    """2 * y * x' = x^2 - y^2 + 1"""
    return params[0]**2 / (2 * params[1]) - params[1] / 2 + 1 / (2 * params[1])


def func4Y(t, params):
    """y' = y + x"""
    return params[1] + params[0]


# ans funcs
def ansFunc4X(t):
    """x = e^(t^2)"""
    return 1 / 2 * t - 1 / 4 * t**2 - 1


def ansFunc4Y(t):
    """y = 1/2 * e^(-t^2)"""
    return 1 + 1 / 4 * t**2
