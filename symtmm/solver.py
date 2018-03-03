#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# solver.py
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
from enum import IntEnum

from symtmm.layers.utils import SV_LENGTH, generic_layer
from symtmm.interfaces.utils import generic_interface
from symtmm.media import Air


class IncompleteDefinitionError(Exception):

    def __init__(self, msg='The definition is incomplete and no analysis can be performed'):
        super().__init__(msg)


SolverState = IntEnum('solver_state', 'INCOMPLETE STRUCTURE BOOTSTRAPED COMPLETE LAMBDIFIED')


class Solver(object):

    def __init__(self, media=None, layers=None, backing=None, saturating_medium=None):

        _omega, _k_x, _theta = sp.symbols('omega k_x theta')
        self.Gref = {
            'syms': {
                'omega': _omega,
                'k_x': _k_x,
                'theta': _theta,
            },
        }

        self.media = media if media is not None else []
        self.layers = layers if layers is not None else []
        self.sat_med = saturating_medium if saturating_medium is not None else Air(self.Gref)
        self.backing = backing

        self.Gref['sat'] = self.sat_med

        self.resultset = []
        self.state = SolverState.INCOMPLETE

    def check_structure(self):
        if self.layers != [] and self.backing is not None:
            self.state = SolverState.STRUCTURE
        else:
            self.state = SolverState.INCOMPLETE

    def check_complete(self):

        if [_ for _ in self.layers if _.medium.is_complete()] == self.layers:
            self.state = SolverState.COMPLETE

    def bootstrap(self):
        """Prepares the linear system in the Symbolic domain"""
        self.check_structure()
        if not self.state >= SolverState.STRUCTURE:
            raise IncompleteDefinitionError("Empty layer list")

        # first layer is fluid (cf Allard & Atalla, 2009, Section 11.5)
        nb_cols = sum(map(lambda _: SV_LENGTH[_.medium.MODEL], self.layers)) + SV_LENGTH[self.sat_med.MODEL]
        last_layer_model = self.layers[-1].medium.MODEL
        if last_layer_model == 'fluid':
            nb_rows = nb_cols-2
        elif last_layer_model == 'elastic':
            nb_rows = nb_cols-3
        elif last_layer_model == 'pem':
            nb_rows = nb_cols-4
        else:
            raise ValueError('Unknown model for the last layer')

        self.A = sp.zeros(nb_rows, nb_cols)

        row_index, col_index = 0, SV_LENGTH[self.sat_med.MODEL]
        for i_L, L in enumerate(self.layers):
            # the first layer is made of the saturating media
            I, J = generic_interface(self.sat_med if i_L == 0 else self.layers[i_L-1], L.medium)()
            M = generic_layer(L.medium)(self.Gref, L.medium, L.thickness)
            self.A[row_index:row_index+I.shape[0], col_index-2:col_index] = I
            self.A[row_index:row_index+I.shape[0], col_index:col_index+M.shape[1]] = J*M

            row_index += I.shape[0]
            col_index += M.shape[1]
        term_matrix = sp.zeros(int(SV_LENGTH[last_layer_model]/2),self.A.shape[1])
        term_matrix[:,-SV_LENGTH[last_layer_model]:] = self.backing(self.layers[-1].medium)
        self.A = self.A.col_join(term_matrix)

        self.state = SolverState.BOOTSTRAPED

    def _extract_Zs(self):
        """ Extraction of the surface impedance, cf Allard & Atalla 2009, eq. 11.88 """
        D1 = self.A.copy()
        D1.col_del(0)
        D2 = self.A.copy()
        D2.col_del(1)
        self.Zs = -D1.det()/D2.det()

    def lambdify(self, params, Gref_values):
        """Creates a functional from an assembled linear system

        params -- list of symbols to be turned into function arguments
        Gref_values -- values to be substituted in the expression (dict)
        """

        # check that general variables are set/flaged as parameters
        check_is_set = lambda t: t[0] in params or t[1] in Gref_values.keys()
        checks = list(map(check_is_set, [
            (self.Gref['syms']['theta'], 'theta'),
            (self.Gref['syms']['omega'], 'omega')
        ]))
        if False in checks:
            raise IncompleteDefinitionError("Some of the parameters aren't constraints")

        self.check_complete()
        if not self.state >= SolverState.COMPLETE:
            raise IncompleteDefinitionError("Incomplete Material")

        self._extract_Zs()
        Zs = self.Zs.copy()

        thickness_subs = {}
        for L in self.layers:
            Zs = Zs.subs(L.medium.get_subs(exclude_list=params))
            thickness_subs[L.thickness] = L.V_thickness
        Zs = Zs.subs(thickness_subs)
        Zs = Zs.subs({
            self.Gref['syms']['k_x']: self.Gref['syms']['omega']/self.sat_med.c*sp.sin(180/sp.pi*self.Gref['syms']['theta'])
        })
        Zs = Zs.subs(self.sat_med.get_subs(exclude_list=params))

        self.V_Gref = {self.Gref['syms'][k]: v for k, v in Gref_values.items() if k != 'k_x'}
        Zs = Zs.subs(Gref_values)

        self.Zs_func = sp.lambdify(params, Zs, 'numpy')
        self.state = SolverState.LAMBDIFIED
        return self.Zs_func
