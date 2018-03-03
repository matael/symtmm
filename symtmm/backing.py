#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# backing.py
#
# This file is part of symtmm, a software distributed under the MIT license.
# For any question, please contact the author below.
#
# Copyright (c) 2017 Mathieu Gaborit <gaborit@kth.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#

import sympy as sp


def rigid(medium):
    if medium.MODEL == 'fluid':
        return sp.Matrix([[0, 1]])
    elif medium.MODEL == 'elastic':
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ])
    elif medium.MODEL == 'pem':
        return sp.Matrix([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
        ])
    else:
        raise ValueError('Type of material not known')
