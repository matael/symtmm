#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# utils.py
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

from .interfaces import\
    fluid_fluid_interface


def generic_interface(medium_left, medium_right):
    """
    Returns a callable to the interface function corresponding to the
    two given media.

    Each interface function then returns a tuple : [I_12], [J_12]
    (see Allard & Atalla, 2009, eq. 11.78)

    Note: interface functions are not symmetrical ( generic_interface(m1, m2) !=
    generic_interface(m2, m1) ).
    """

    if medium_left.MODEL == 'fluid':
        if medium_right.MODEL == 'fluid':
            return fluid_fluid_interface
