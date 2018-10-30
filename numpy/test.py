# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# 练习：实现一个函数，去除字符串首位空格，注意不要使用strip()


def make(s):
    for i in s[:]:
        if i == ' ':
            s = s[1:]
        else:
            break
    for i in s[::-1]:
        if i == ' ':
            s = s[:-1]
        else:
            break
    return s
a = [x for x in range(2, 101) if not [y for y in range(2, x) if x % y == 0]]
print(a)
