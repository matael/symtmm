#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# air.py
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

import numpy as np

from .medium import Medium


class Air(Medium):

    MEDIUM_TYPE = 'fluid'
    MODEL = MEDIUM_TYPE

    EXPECTED_PARAMS = [
        ('T', float),
        ('P', float),
        ('gamma', float),
        ('lambda_', float),
        ('mu', float),
        ('Pr', float),
        ('molar_mass', float),
        ('rho', float),
        ('C_p', float),
        ('K', float),
        ('c', float),
        ('Z', float),
        ('C_v', float),
        ('nu', float),
        ('nu_prime', float),
    ]

    def __init__(self, global_refs):
        super().__init__(global_refs)

        self.V['T'] = 293.15  # reference temperature [K]
        self.V['P'] = 1.01325e5  # atmospheric Pressure [Pa]
        self.V['gamma'] = 1.400  # polytropic coefficient []
        self.V['lambda_'] = 0.0262  # thermal conductivity [W.m^-1.K^-1]
        self.V['mu'] = 0.1839e-4  # dynamic viscosity [kg.m^-1.s^-1]
        self.V['Pr'] = 0.710  # Prandtl's number []
        self.V['molar_mass'] = 0.29e-1  # molar mass [kg.mol^-1]
        self.V['rho'] = 1.213  # density [kg.m^-3]
        self.V['C_p'] = 1006  # (mass) specific heat capacity as constant pressure [J.K^-1]

        self.V['K'] = self.V['gamma']*self.V['P']  # adiabatic bulk modulus
        self.V['c'] = np.sqrt(self.V['K']/self.V['rho'])  # adiabatic sound speed
        self.V['Z'] = self.V['rho']*self.V['c']  # characteristic impedance
        self.V['C_v'] = self.V['C_p']/self.V['gamma']  # (mass) specific heat capacity as constant volume [J.K^-1]
        self.V['nu'] = self.V['mu']/self.V['rho']  # kinematic viscosity [m.s^-2]
        self.V['nu_prime'] = self.V['nu']/self.V['Pr']  # viscothermal losses
