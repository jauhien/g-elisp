#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections, argparse
from pyparsing import *

#repository parser

Package = collections.namedtuple("Package", "name version deps desc type")
Dependency = collections.namedtuple("Dependency", "name version")

LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR, HEX, PT, ONE = map(Suppress, "()[]{}|#.1")

NIL = (Literal("nil") | Literal("()")).setParseAction(lambda s, l, t : [[]])
pkg_name = Word(alphanums + "_-+.")
pkg_vers = (LPAR + Word(nums + " ") + RPAR).setParseAction(lambda s, l, t: [t[0].replace(' ','.')])
pkg_desc = dblQuotedString.setParseAction(removeQuotes)
pkg_type = Literal("single") | Literal("tar")
pkg_depn = (LPAR + pkg_name + pkg_vers + RPAR).setParseAction(lambda s, l, t : [Dependency(t[0], t[1])])
pkg_deps = (LPAR + OneOrMore(pkg_depn) + RPAR).\
           setParseAction(lambda s, l, t: [[i for i in t]])\
           | NIL
package  = (LPAR + pkg_name + PT + LBRK + pkg_vers + pkg_deps + pkg_desc + pkg_type + RBRK + RPAR)\
           .setParseAction(lambda s, l ,t: [Package(t[0], t[1], t[2], t[3], t[4])])
repo     = (LPAR + ONE + OneOrMore(package) + RPAR)


def parse_repo(f):
    return repo.parseFile(f)

#end of repository parser

#config parser

EQ            = Suppress('=') 
cfg_line      = Group(Word(printables) + EQ + Word(printables))
cfg_file      = OneOrMore(cfg_line)

#end config parser

#arguments parser

Argument = collections.namedtuple("Argument", "arg nargs")
Arguments = collections.namedtuple("Arguments", "args sub")
Command_group = collections.namedtuple("Command_group", "command help args sub")
Command = collections.namedtuple("Command", "command help args func")

def create_argsubparser(subparsers, command):
    subparser = subparsers.add_parser(command.command, help=command.help)
    for arg in command.args:
        subparser.add_argument(arg.arg, nargs=arg.nargs)

    if type(command) is Command:
        subparser.set_defaults(func=command.func)
    elif type(command) is Command_group:
        if command.sub != []:
            nextparsers = subparser.add_subparsers()
        for sub in command.sub:
            create_argsubparser(nextparsers, sub)
    else:
        raise Exception
    return subparser        

def create_argparser(arguments):
    if not type(arguments) is Arguments:
        raise Exception
    parser = argparse.ArgumentParser()
    for arg in arguments.args:
        parser.add_argument(arg.arg, nargs=arg.nargs)
    if arguments.sub != []:
        subparsers = parser.add_subparsers()
    for sub in arguments.sub:
        create_argsubparser(subparsers, sub)

    return parser

def parse_args(args):
    return create_argparser(args).parse_args()
            
#end argument parser
