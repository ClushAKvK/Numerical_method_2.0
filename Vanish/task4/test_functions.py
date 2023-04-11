import math

# Test 1
def px1(x):
    return 1

def fx1(x):
    return -x

def ansFunc1(x):
    return math.sin(x) / math.sin(1) - x


# Test 2
def px2(x):
    return -4

def fx2(x):
    return 16 * x * math.e**(2*x)

def ansFunc2(x):
    return 1 - x


# Test 3
def px3(x):
    return 4

def fx3(x):
    return math.sin(2 * x) + 1

def ansFunc3(x):
    return 1 - x