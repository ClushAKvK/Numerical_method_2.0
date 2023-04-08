import math

def zero_f(x):
    return 0
    # return math.sin(math.pi * x)

# Test 1

def start_1(x):
    # return 3 - x + math.cos(3 * math.pi * x / 4)
    return math.sin(math.pi * x)

def border_left_1(t):
    # return 1
    return 0

def border_right_1(t):
    # return 1
    return 0

def ans_func_1(t, x):
    return math.e**(-math.pi**2 * t) * math.sin(math.pi * x)


# Test 2

def f_2(x):
    return math.sin(math.pi * x)

def start_2(x):
    # return 3 - x + math.cos(3 * math.pi * x / 4)
    return 0

def border_left_2(t):
    # return 1
    return 0

def border_right_2(t):
    # return 1
    return 0

def ans_func_2(t, x):
    return (1 / math.pi**2) * (1 - math.e**(-math.pi**2 * t)) * math.sin(math.pi * x)


# Test 3

def start_3(x):
    # return 3 - x + math.cos(3 * math.pi * x / 4)
    return 0

def border_left_3(t):
    # return 1
    return 0

def border_right_3(t):
    # return 1
    return 1

# def ans_func_1(t, x):
#     return math.e**(-math.pi**2 * t) * math.sin(math.pi * x)

# Test 4

def start_4(x):
    # return 3 - x + math.cos(3 * math.pi * x / 4)
    return 10 - x

def border_left_4(t):
    # return 1
    return 3

def border_right_4(t):
    # return 1
    return 0

# Test 5
def start_5(x):
    return 1

def border_left_5(t):
    return 1

def border_right_5(t):
    return 0

def border_right_6(t):
    return math.sin(math.pi * t)