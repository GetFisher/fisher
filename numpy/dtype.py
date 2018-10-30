# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np

# a = np.array([1, 2, 3, 4, 5], dtype=np.int8)
# print('a.dtype:', a.dtype)

# b = a.astype(np.float_)
# print('b.dtype:', b.dtype)

# c = a.astype(np.float32)
# print('c.dtype:', c.dtype)

# d = c.astype(np.str_)
# print('d.dtype:', d.dtype)


# # e = np.array([1234], dtype=np.int32)
# # e = np.array([1234], dtype='int32')
# e = np.array([1234], dtype='i4')
# print(e.dtype, e.shape)

# f = np.array((['1234'], ['567']), dtype=(np.str_, 0))
# print('f', f.dtype, f[1])

# g = np.array([(1, 2, 3, 4)], dtype=(np.int32, 4))
# print('g', g.dtype, g.shape)
# g = np.array([((1, 2), (3, 4))], dtype=(np.int32, (2, 2)))
# print('g', g.dtype, g.shape)
# print(g)

# h = np.array([('1234', (1, 2, 3, 4))], dtype='U4,4i4')
# print('h', h.dtype, h[0]['f0'], h[0]['f1'])

# i = np.array([('1234', (1, 2, 3, 4)), ('5678', (5, 6, 7, 8))],
#              dtype={'names': ['fa', 'fb'], 'formats': ['U4', '4i4']})

# print('i:', i.shape, i.dtype, i[0]['fa'], i[0]['fb'])

# j = np.array([('1234', (1, 2, 3, 4))], dtype=[
#              ('fa', np.str_, 4), ('fb', np.int32, 4)])
# print('j:', j.shape, j.dtype, j[0]['fa'], j[0]['fb'])

# k = np.array([('1234', (1, 2, 3, 4))], dtype=[
#              ('fa', 'U4'), ('fb', '4i4')])
# print('k:', k.shape, k.dtype, k[0]['fa'], k[0]['fb'])


# # 基本类型，解释类型
# l = np.array([0x1234], dtype=(
#     '>u2', {'names': ['lo', 'hi'], 'formats': ['u1', 'u1']}))
# # 0x表示为16进制数，'u1'整型一个字节
# # 16进制数的一个位相当于二进制的4位，所以4位16进制是两个字节
# # 低地址拿到的是高数位的12，高地址拿到的是低数为34
# print('{:x},{:x},{:x}'.format(l[0], l['lo'][0], l['hi'][0]))
m = np.array(['python'], dtype=(
    'U5', {'names': ['codes'], 'formats': ['5u4']}))
print(m[0], m['codes'])
# a = np.arange(1, 8)
# b = np.arange(2, 9)
# c = a + b
# print(c)
# d = a * b
# print(d)
# e = c * 0.5
# print(e)
