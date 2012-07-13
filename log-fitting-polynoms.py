#!/usr/bin/env python
"""Print fitting polynoms in a log/log form for common functions."""
import numpy as np

def log_fitting_polynom(x, y):
    assert x.shape == y.shape
    # find approximating polynom in a form log(y) = a*log(x) + b
    logsafe = np.logical_and(x>0, y>0)
    logx = np.log2(x[logsafe])
    logy = np.log2(y[logsafe])
    coeffs = np.polyfit(logx, logy, deg=1)
    return str(np.poly1d(coeffs, variable='log2(N)')).strip()

x = np.fromiter((10**n for n in range(7)), dtype=np.float)
f = log_fitting_polynom
print 'log2(N)           ', f(x, np.log2(x))
print 'log2(N)*log2(N)   ', f(x, np.log2(x)*np.log2(x))
print 'sqrt(N)           ', f(x, np.sqrt(x))
print 'N**0.8            ', f(x, x**0.8)
print 'N                 ', f(x, x)
print 'N*log2(N)         ', f(x, x*np.log2(x))
print 'N*log2(N)*log2(N) ', f(x, x*np.log2(x)*np.log2(x))
print 'N*N               ', f(x, x*x)
