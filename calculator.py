"""
Assignment 6
Yu-Fen Chiu

original_time: avg(9.62329, 8.71107, 10.1175) = 9.483953 s
optimized_time: avg(0.0173354, 0.0453904, 0.0394148) = 0.03404687 s
speedup = 9.483953 / 0.03404687 = 278.5558 times

output from line_profiler:
(1)
Total time: 9.62329 s
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    48                                           def hypotenuse(x,y):
    53         1      5264903 5264903.0     40.1      xx = multiply(x,x)
    54         1      2769889 2769889.0     21.1      yy = multiply(y,y)
    55         1      2552908 2552908.0     19.4      zz = add(xx, yy)
    56         1      2538774 2538774.0     19.3      return sqrt(zz)
(2)
Total time: 0.0939509 s
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    58                                           def hypotenuse_opt(x,y):
    63         1        21490  21490.0     16.8      xx = np.square(x)
    64         1        33210  33210.0     25.9      yy = np.square(y)
    65         1        47348  47348.0     36.9      zz = np.add(xx, yy)
    66         1        26104  26104.0     20.4      return np.sqrt(zz)
(3)
Total time: 0.0173354 s
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    95                                           def hypotenuse_opt2(x,y):
   100         1         4917   4917.0     20.8      xx = np.multiply(x,x)
   101         1         5049   5049.0     21.4      yy = np.multiply(y,y)
   102         1         6806   6806.0     28.8      zz = np.add(xx, yy)
   103         1         6874   6874.0     29.1      return np.sqrt(zz)

To optimize the task, I used NumPy build-in function instead of user-defined functions.
np.square(), np.multiply(), np.add(), and np.sqrt() are applied in optimized function.
And it turned out that np.multiply() was slightly faster than np.square() in my case.
So hypotenuse_opt2(x,y) will be the one comparing to hypotenuse(x,y) to calculate speedup!

"""

# -----------------------------------------------------------------------------
# calculator.py
# -----------------------------------------------------------------------------  
import numpy as np

def add(x,y):
    """
    Add two arrays using a Python loop.
    x and y must be two-dimensional arrays of the same shape.
    """
    m,n = x.shape
    z = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            z[i,j] = x[i,j] + y[i,j]
    return z


def multiply(x,y):
    """
    Multiply two arrays using a Python loop.
    x and y must be two-dimensional arrays of the same shape.
    """
    m,n = x.shape
    z = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            z[i,j] = x[i,j] * y[i,j]
    return z


def sqrt(x):
    """
    Take the square root of the elements of an arrays using a Python loop.
    """
    from math import sqrt
    m,n = x.shape
    z = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            z[i,j] = sqrt(x[i,j])
    return z

def hypotenuse(x,y):
    """
    Return sqrt(x**2 + y**2) for two arrays, a and b.
    x and y must be two-dimensional arrays of the same shape.
    """
    xx = multiply(x,x)
    yy = multiply(y,y)
    zz = add(xx, yy)
    return sqrt(zz)

def hypotenuse_opt(x,y):
    """
    Return sqrt(x**2 + y**2) for two arrays, a and b.
    x and y must be two-dimensional arrays of the same shape.
    """
    xx = np.square(x)
    yy = np.square(y)
    zz = np.add(xx, yy)
    return np.sqrt(zz)

def hypotenuse_opt2(x,y):
    """
    Return sqrt(x**2 + y**2) for two arrays, a and b.
    x and y must be two-dimensional arrays of the same shape.
    """
    xx = np.multiply(x,x)
    yy = np.multiply(y,y)
    zz = np.add(xx, yy)
    return np.sqrt(zz)

# -----------------------------------------------------------------------------
# calculator_test.py
# ----------------------------------------------------------------------------- 
import numpy as np

M = 10**3
N = 10**3

A = np.random.random((M,N))
B = np.random.random((M,N))

%lprun -f hypotenuse hypotenuse(A,B)
%lprun -f hypotenuse_opt hypotenuse_opt(A,B)
%lprun -f hypotenuse_opt2 hypotenuse_opt2(A,B)