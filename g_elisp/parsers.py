#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

import collections
from pyparsing import *

#repository parser

Attributes = collections.namedtuple("Attributes", "realname deps desc type")
Package = collections.namedtuple("Package", "name version")

LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR, HEX, PT, ONE = map(Suppress, "()[]{}|#.1")

NIL = (Literal("nil") | Group(LPAR + RPAR)).setParseAction(lambda s, l, t : [[]])
pkg_name = Word(alphanums + "_-+.")
pkg_vers = (LPAR + Word(nums + " -") + RPAR).\
           setParseAction(lambda s, l, t: [t[0].replace(' ','.').replace('-','')])
pkg_desc = dblQuotedString.setParseAction(removeQuotes)
pkg_type = Literal("single") | Literal("tar")
pkg_depn = (LPAR + pkg_name + pkg_vers + RPAR).setParseAction(lambda s, l, t : [Package(t[0], t[1])])
pkg_deps = (LPAR + OneOrMore(pkg_depn) + RPAR).\
           setParseAction(lambda s, l, t: [[i for i in t]])\
           | NIL
pkg_attr = (pkg_deps + pkg_desc + pkg_type + RBRK)\
           .setParseAction(lambda s, l ,t: [Attributes('', t[0],
                                            ''.join( c for c in t[1] if c not in '"\'`{}$\\'),
                                            t[2])])
pkg      = (pkg_name + PT + LBRK + pkg_vers)\
           .setParseAction(lambda s, l ,t: [Package(t[0], t[1])])
repo     = Dict(LPAR + ONE + OneOrMore(Group(LPAR + pkg + pkg_attr + RPAR)) + RPAR)

#end of repository parser
