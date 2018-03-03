#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# medium.py
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
from enum import Enum


MediumState = Enum('medium_state', 'INCOMPLETE COMPLETE')


class Medium(object):
    """ Holds a medium definition and allows its manipulation and loading """

    EXPECTED_PARAMS = []
    OPT_PARAMS = []
    MEDIUM_TYPE = 'generic'
    MODEL = ''

    def __init__(self, global_refs):
        self.omega = -1
        self.name = 'Generic Medium'

        param_names = list(map(lambda _: _[0], self.__class__.EXPECTED_PARAMS+self.__class__.OPT_PARAMS))

        tmp_symbolset = sp.symbols(' '.join(param_names))

        self.V = {_: None for _ in param_names}
        self.syms = {pname: tmp_symbolset[i_p] for i_p, pname in enumerate(param_names)}
        self.Gref = global_refs
        self.state = MediumState.INCOMPLETE
        self.is_complete = lambda: self.state == MediumState.COMPLETE

    def __str__(self):
        return f'{self.name} (type: {self.__class__.MEDIUM_TYPE}, model: {self.__class__.MODEL})'

    def __getattr__(self, n):
        try:
            return self.syms[n]
        except KeyError:
            raise AttributeError(f'{n} is neither an attribute of {self.__class__} object nor an inner symbol.')

    def update_frequency(self, omega):
        """ Computes parameters' value for the given circular frequency """
        pass

    def _compute_missing(self):
        pass

    def from_dict(self, parameters):
        """Reads medium definition from a hashmap of params.
        Raises a LookupError if the parameter definition is incomplete."""

        for param, param_type in self.__class__.EXPECTED_PARAMS:
            param_value = parameters.get(param)
            if param_value is None:
                raise LookupError(f'Unable to find definition of parameter "{param}"')
            else:
                self.V[param] = param_type(param_value)
        for param, param_type in self.__class__.OPT_PARAMS:
            param_value = parameters.get(param)
            if param_value is not None:
                self.V[param] = param_type(param_value)
        self.name = parameters.get('name', "Unnamed Medium")
        self._compute_missing()
        self.state = MediumState.COMPLETE

    def get_subs(self, exclude_list=[]):
        return {self.syms[_]: self.V[_] for _ in self.syms.keys() if not self.syms[_] in exclude_list}
