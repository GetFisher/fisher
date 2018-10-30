# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np

a = np.array([[1 + 1j, 2 + 4j, 3 + 7j],
              [4 + 2j, 5 + 5j, 6 + 8j],
              [7 + 3j, 8 + 6j, 9 + 9j]
              ])
print('a.dtype')
print(a.dtype)  # complex128
print('a.dtype.char')  # D
print(a.dtype.char)

print('a.dtype.str')  # <c16
print(a.dtype.str)

print('a.dtype.name')  # <c16
print(a.dtype.name)  # complex128

print('a.shape')
print(a.shape)  # (3, 3)

print('a.ndim')
print(a.ndim)  # 2

print('a.size')
print(a.size)  # 9

print('a.itemsize')
print(a.itemsize)  # 16

print('a.nbytes')
print(a.nbytes)  # 16*9=144

print('a.real')
print(a.real)

print('a.imag')
print(a.imag)

print('a.T')
print(a.T)

print('flat')
for i in a.flat:  # 性能最好，迭代器，惰性
    print(i)


print('ravel')
for i in a.ravel():  # 性能居中
    print(i)


print('flatten')
for i in a.flatten():  # 性能最差，创建一个容器，既有元数据也有拷贝数据
    print(i)

b = a.tolist()  # 数组转换为列表
print('b')
print(b)

c = np.array(b)  # 装换位数组
print('c')
print(c)

d = []
for i in range(10):
    d.append(i)
print(d)

e = np.array([], dtype=int)
for i in range(10):
    e = np.append(e, i)
print('e')
print(e)

# 等需要频繁追加元素时，可以先用列表来追加元素，最后再转换成数组
