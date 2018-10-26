from numpy import *

a = array([[1, 2, 3], [4, 5, 6],[7,8,9]])
print a.ndim
print a.shape
b = tile(a, 4)
print a
print b
print b.ndim
print b.shape

c = tile(a, (2, 3))
print c
print c.shape
print c.ndim
