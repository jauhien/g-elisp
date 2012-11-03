#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyparsing import *

#repository parser

LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR, HEX, PT = map(Suppress, "()[]{}|#.")

s_decimal     = Word(nums).setParseAction(lambda s, l, t: [int(t[0])]);
s_token       = Word(alphanums + "-./_:*+=")
s_hexadecimal = HEX + OneOrMore(Word(hexnums))\
                .setParseAction(lambda s, l, t: int("".join(t), 16)) + HEX

s_string      = s_decimal | s_token | s_hexadecimal \
                | dblQuotedString.setParseAction(removeQuotes)

s_exp         = Forward()
s_list        = Group(LPAR + ZeroOrMore(s_exp) + RPAR)
s_vector      = Group(LBRK + ZeroOrMore(s_exp) + RBRK)
s_exp        << (s_vector | s_string | Group(LPAR + s_exp + PT + s_exp + RPAR) | s_list)

#end of repository parser

#config parser

EQ            = Suppress('=') 
cfg_line      = Group(Word(printables) + EQ + Word(printables))
cfg_file      = OneOrMore(cfg_line)

#end config parser
