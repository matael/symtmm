#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# layer.py
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


class Layer(object):

    def __init__(self, medium, thickness, name="Unnamed Layer"):
        self.thickness = sp.symbols('d')
        self.V_thickness = thickness
        self.medium = medium
        self.name = name

    def __str__(self):
        return f'{self.name} - {self.thickness}m of {self.medium.name} (self.medium.MEDIUM_TYPE)'
