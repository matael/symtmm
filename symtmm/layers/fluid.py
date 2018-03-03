#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# fluid.py
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


def fluid_layer(global_refs, medium, d):

    if medium.MEDIUM_TYPE == 'eqf':
        rho = medium.rho_eq_til
        c = medium.c_eq_til
    elif medium.MEDIUM_TYPE == 'fluid':
        rho = medium.rho
        c = medium.c
    else:
        raise ValueError('Provided material is not a fluid')

    omega = global_refs['syms']['omega']
    k_z = sp.sqrt((omega/c)**2 - global_refs['syms']['k_x']**2)
    return sp.Matrix([
        [sp.cos(k_z*d), 1j*omega*rho/k_z*sp.sin(k_z*d)],
        [1j*k_z/(omega*rho)*sp.sin(k_z*d), sp.cos(k_z*d)]
    ])
