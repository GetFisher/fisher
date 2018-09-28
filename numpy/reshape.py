# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np

a = np.arange(1, 9)
print(a.shape, a, sep='\n')
print('---------------------')
b = a.reshape((2, 4))
print(b.shape, b, sep='\n')
print('---------------------')
print(a.shape, a, sep='\n')
b.shape = (4, 2)
print(b.shape, b, sep='\n')
print('---------------------')
c = b.reshape((2, 2, 2))
print(c.shape, c, sep='\n')
c.shape = 8
print(c.shape, c, sep='\n')
