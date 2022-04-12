#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
# Copyright (C) 2015 su_v, suv-sf@users.sf.net
# Copyright (C) 2022 KT, code@acme-enterprises.co.uk
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

################################
# Root Branch generator
###############################

# from turtle import * as pturtle

# ELTYPE - Type Root or Branch ELTYPE dropdown giving value - 1 or 1
# ELQTY - How many roots ELQTY int
# WO - Wonkiness WO make 1 to start with, work on the wonkines.. int This is number of twists and turns
# SPIKY - Spikiness is deviation for each twist and then getting smaller towards the end SPIKY
# MAXL - Maximum length MAX int
# MINL - Minimum length MIN int
# ELLENGTH - Length ELLENGTH float this is random number between MIN MAX
# RANDANGLE - Angle to go in RANDANGLE
# STARTSTROKE - Start stroke width STARTSTROKE float
# ENDSTROKE - End stroke width ENDSTROKE float

"""
eltype
elqty
wo
spiky
maxl
minl
startstroke
endstroke
pentoggle
"""

import math
# import cmath
from math import cos, degrees, sin
import random
# import turtle

from sqlite3 import IntegrityError
import inkex
from inkex import turtle as pturtle
from inkex import PathElement
from inkex import SvgDocumentElement
from inkex import Group
from inkex import bezier, PathElement, CubicSuperPath
#import simplestyle
#import simpletransform


class RootBranch(inkex.Effect):
    def add_arguments(self, pars):
        pars.add_argument("--eltype", type=int, default="Root",
                          help="root or branch?")
        pars.add_argument("--elqty", type=int, default=20,
                          help="num elemenets required")
        pars.add_argument("--wo", type=int, default=1,
                          help="set the wonkiness")
        pars.add_argument("--spiky", type=int, default=4,
                          help="set the spikiness")
        pars.add_argument("--maxl", type=int, default=300,
                          help="max element length")
        pars.add_argument("--minl", type=int, default=50,
                          help="min element length")
        pars.add_argument("--startstroke", type=float, default=5.0,
                          help="stroke size to start with")
        pars.add_argument("--endstroke", type=float, default=1.0,
                          help="stroke size to end with")
        pars.add_argument("--pentoggle", type=inkex.Boolean,
                          default=False, help="Lift pen for backward steps")

    def effect(self):
        # def generate(self):

        eltype = self.options.eltype

        elqty = self.options.elqty

        wonkiness = self.options.wo

        numpaths = 1

        svg = self.document.getroot()
        page_w_mid = self.svg.unittouu(svg.get('width')) / 2
        page_h_mid = self.svg.unittouu(svg.get('height')) / 2

        minl = self.options.minl
        maxl = self.options.maxl

        # set stroke width
        startstroke = self.options.startstroke

        # inkex.utils.debug(centrepoint)

        if(maxl < minl):
            maxl = minl

        # generate random angle (deg)
        randangle = random.randrange(0, 179)

        x1 = page_w_mid
        y1 = page_h_mid

        layer = self.svg.get_current_layer().add(inkex.Group.new('RootBranch_Layer'))

        #parent = layer

        for x in range(0, elqty):
            # set element length
            ellength = random.randrange(minl, maxl)
            randangle = random.randrange(20, 160)

            x2 = ellength * float(cos(math.radians(randangle)))
            y2 = ellength * float(sin(math.radians(randangle)))

            x2 = x2 + page_w_mid
            y2 = y2 + page_h_mid

            """
            inkex.utils.debug("RA: (deg) " + str(randangle))
            inkex.utils.debug("RA: (rad) " + str(math.radians(randangle)))
            inkex.utils.debug("R30: " + str(rad_30))

            inkex.utils.debug("x3: " + str(x3))
            inkex.utils.debug("y2: " + str(y2))
            """
            # inkex.utils.debug("x2: " + str(x2))
            # inkex.utils.debug("y2: " + str(y2))
            # inkex.utils.debug("el lenght: " + str(ellength))
            # inkex.utils.debug("x2: " + str(x2) + " y2: " + str(y2))

            # x2 = random.randrange(0, 1000)
            # y2 = random.randrange(500, 800)

            pathid = "RB_Path_" + str(numpaths)
            line = layer.add(PathElement(id=pathid))
            line.style = {'stroke': '#000000',
                          'stroke-width': str(startstroke), 'fill': 'none', 'stroke-linecap': 'round',
                          'stroke-linejoin': 'miter', 'stroke-opacity': 1}
            line.path = 'M ' + str(x1) + ',' + str(y1) + \
                ' L ' + str(x2) + ',' + str(y2)

            # if not self.options.ids:
            # return inkex.errormsg(_("Please select an object"))
            # if not self.svg.selected:
            #    raise inkex.AbortExtension("Please select an object.")

            # for node in self.svg.selection.filter(PathElement):
            for node in self.svg.selection.get(inkex.PathElement(pathid)):
                new = []
                for sub in node.path.to_superpath():
                    new.append([sub[0][:]])
                    i = 1
                    while i <= len(sub) - 1:
                        length = bezier.cspseglength(new[-1][-1], sub[i])

                        # got from addnodes.py
                        splits = math.ceil(length / wonkiness)

                        for sel in range(int(splits), 1, -1):
                            result = bezier.cspbezsplitatlength(
                                new[-1][-1], sub[i], 1.0 / sel)
                            better_result = [[list(el) for el in elements]
                                             for elements in result]
                            new[-1][-1], nxt, sub[i] = better_result
                            new[-1].append(nxt[:])
                        new[-1].append(sub[i])
                        i += 1
                node.path = CubicSuperPath(new).to_path(curves_only=True)

            # select line
            # do stroke to path
            numpaths = numpaths + 1
        # do select all on layer
        # do Path Combine


if __name__ == '__main__':
    RootBranch().run()
