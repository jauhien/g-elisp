#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
from pyparsing import *

#repository parser

Attributes = collections.namedtuple("Attributes", "version deps desc type")
Dependency = collections.namedtuple("Dependency", "name version")

LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR, HEX, PT, ONE = map(Suppress, "()[]{}|#.1")

NIL = (Literal("nil") | Literal("()")).setParseAction(lambda s, l, t : [[]])
pkg_name = Word(alphanums + "_-+.")
pkg_vers = (LPAR + Word(nums + " ") + RPAR).setParseAction(lambda s, l, t: [t[0].replace(' ','.')])
pkg_desc = dblQuotedString.setParseAction(removeQuotes)
pkg_type = Literal("single").setParseAction(lambda s, l, t: ["el"]) | Literal("tar")
pkg_depn = (LPAR + pkg_name + pkg_vers + RPAR).setParseAction(lambda s, l, t : [Dependency(t[0], t[1])])
pkg_deps = (LPAR + OneOrMore(pkg_depn) + RPAR).\
           setParseAction(lambda s, l, t: [[i for i in t]])\
           | NIL
pkg_attr = (PT + LBRK + pkg_vers + pkg_deps + pkg_desc + pkg_type + RBRK)\
           .setParseAction(lambda s, l ,t: [Attributes(t[0], t[1], t[2], t[3])])
repo     = Dict(LPAR + ONE + OneOrMore(Group(LPAR + pkg_name + pkg_attr + RPAR)) + RPAR)

def parse_repo(f):
    return repo.parseFile(f)

#end of repository parser
