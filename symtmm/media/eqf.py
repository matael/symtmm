#! /usr/bin/env python
# -*- coding:utf8 -*-
# eqf.py
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

from .medium import Medium


class Eqf(Medium):

    MEDIUM_TYPE = 'eqf'
    MODEL = 'fluid'
    EXPECTED_PARAMS = [
        ('phi', float),  # Porosity
        ('sigma', float),  # Flow resistivity
        ('alpha', float),  # Tortuosity
        ('Lambda_prime', float),  # Thermal characteristic length
        ('Lambda', float),  # Viscous characteristic length
        ('rho_1', float),  # Mass of solid per unit volume of aggregate
        ('nu', float),  # poisson ratio
        ('E', float),  # Young's modulus
        ('eta', float)  # viscosity
    ]

    def __init__(self, global_refs):
        super().__init__(global_refs)

        omega = self.Gref['syms']['omega']
        Air = self.Gref['sat']

        #  Johnson et al model for rho_eq_til
        self.omega_0 = self.sigma*self.phi/(Air.rho*self.alpha)
        self.omega_infty = (self.sigma*self.phi*self.Lambda)**2/(4*Air.mu*Air.rho*self.alpha**2)
        self.F_JKD = sp.sqrt(1+1j*omega/self.omega_infty)
        self.rho_eq_til = (Air.rho*self.alpha/self.phi)*(1+(self.omega_0/(1j*omega))*self.F_JKD)
        self.alpha_til = self.phi*self.rho_eq_til/Air.rho

        #  Champoux-Allard model for K_eq_til
        self.omega_prime_infty = (16*Air.nu_prime)/(self.Lambda_prime**2)
        self.F_prime_CA = sp.sqrt(1+1j*omega/self.omega_prime_infty)
        self.alpha_prime_til = 1+self.omega_prime_infty*self.F_prime_CA/(2*1j*omega)
        self.K_eq_til = (Air.gamma*Air.P/self.phi)/(Air.gamma-(Air.gamma-1)/self.alpha_prime_til)

        self.c_eq_til = sp.sqrt(self.K_eq_til/self.rho_eq_til)

    def _compute_missing(self):
        self.V['N'] = self.V['E']/(2*(1+self.V['nu']))
