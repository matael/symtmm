#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# interfaces.py
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


def fluid_fluid_interface():
    return sp.eye(2), sp.eye(2)
