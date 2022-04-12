#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
# Copyright (C) 2015 su_v, suv-sf@users.sf.net
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
# Mini Lindenmayer tool
###############################

# from turtle import * as pturtle

import inkex
from inkex import turtle as pturtle


class TurtleRtree(inkex.GenerateExtension):

    def add_arguments(self, pars):
        pars.add_argument("--size", type=float, default=100.0,
                          help="initial branch size")
        pars.add_argument("--minimum", type=float, default=4.0,
                          help="minimum branch size")
        pars.add_argument("--pentoggle", type=inkex.Boolean, default=False,
                          help="Lift pen for backward steps")
        pars.add_argument("--branchlength", type=float, default=4.0,
                          help="minimum branch length")
        pars.add_argument("--branchwidth", type=float, default=4.0,
                          help="minimum branch width")

        # self.options.numtimes

    def generate(self):
        self.options.size = self.svg.unittouu(str(self.options.size) + 'px')
        self.options.minimum = self.svg.unittouu(
            str(self.options.minimum) + 'px')
        point = self.svg.namedview.center

        style = inkex.Style({
            'stroke-linejoin': 'miter', 'stroke-width': str(self.svg.unittouu('1px')),
            'stroke-opacity': '1.0', 'fill-opacity': '1.0',
            'stroke': '#000000', 'stroke-linecap': 'round',
            'fill': 'Blue'
        })

        tur = pturtle.pTurtle()
        tur.pu()
        # getting the main SVG document element (canvas)
        svg = self.document.getroot()

        # getting the width and height attributes of the canvas
        # canvas_width = self.svg.unittouu(svg.get('width')) / 2
        # canvas_height = self.svg.unittouu(svg.attrib['height'] / 2)
        canvas_width = self.svg.get('width')
        canvas_height = self.svg.attrib['height']

        canvas_width = 1000
        canvas_height = 1000

        canvas_width_half = float(canvas_width / 2)
        canvas_height_half = float(canvas_height / 2)

        # tur.setpos(point)
        tur.setpos(point)
        tur.pd()
        tur.rtree(self.options.size, self.options.minimum,
                  self.options.pentoggle)
        return inkex.PathElement(d=tur.getPath(), style=str(style))

    def replace(seq, replacementRules, n):
        for i in range(n):
            newseq = ""
            for element in seq:
                newseq = newseq + replacementRules.get(element, element)
            seq = newseq
        return seq

    def draw(commands, rules):
        for b in commands:
            try:
                rules[b]()
            except TypeError:
                try:
                    draw(rules[b], rules)
                except:
                    pass

    # def main():
    ################################
    # Example 1: Snake kolam
    ################################

    def r():
        right(45)

    def l():
        left(45)

    def f():
        forward(7.5)

    # snake_rules = {"-": r, "+": l, "f": f, "b": "f+f+ff--f+f+f"}
    # snake_replacementRules = {"b": "b+f+b--f--b+f+b"}

    """
    snake_rules = {"-": r, "+": l, "f": f, "b": "ffff-ff+"}
    snake_replacementRules = {"b": "b"}
    snake_start = "b--f--b--f"

    drawing = replace(snake_start, snake_replacementRules, 3)

    reset()
    speed(3)
    tracer(1, 0)
    ht()
    up()
    backward(195)
    down()
    draw(drawing, snake_rules)

    return "Done!"
    """


if __name__ == '__main__':
    TurtleRtree().run()

"""

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()
"""
