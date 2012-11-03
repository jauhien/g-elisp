#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
g-driver interface

g-common uses appropriate g-driver to have the job done

- g-driver GAPI

print GAPI -- API of g-driver, currently 0

- g-driver <overlay> sync <url>

synchronize overlay

overlay -- path to overlay

url -- repository url

- g-driver <overlay> list-packages

list packages from overlay in the format
<category>/<package> <version>
one package per line

- g-driver <overlay> list-categories

list categories from overlay

- g-driver <overlay> package <category>/<package> <version> [<var>]

list variables for given package

If var argument is given g-driver should print value for this variable or None if it is not set

If var is not given g-driver should print a list of variables (one per line) in form
<variable name> = <value>

Variables are those that must be set in ebuild
and GCOMMON_PHASES (ebuild function that g-driver will handle)

Obligatory variables are: EAPI, SRC_URI, GCOMMON_PHASES

- g-driver <overlay> phase <category>/<package> <version> <ebuild-function>

print source code for a given ebuild function

g-driver should print source code only for functions previously returned by package command, for other functions it can print just new line or nothing

- g-driver ebuild <ebuild-function>

handle given ebuild function, env variables must be set appropriately

'''

import sys
from urllib import request

from parsers import s_exp, cfg_file
from files import *

class GElispError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def sync(overlay, url):
    datadir = get_datadir(overlay)
    if not os.path.exists(datadir):
        os.makedirs(datadir)
        
    arcfile = get_arcfile(overlay)
    archive_contents = url + '/archive-contents'
    h = request.urlopen(archive_contents)
    f = open(arcfile, 'wb')
    f.write(h.read())
    h.close()
    f.close()

    cfgfile = get_cfgfile(overlay)
    f = open(cfgfile, 'wb')
    f.write(bytes("url = " + url, 'UTF-8'))
    f.close()
    return 0
    

def list_packages(overlay):
    f = open(get_arcfile(overlay), 'r')
    t = s_exp.parseFile(f)[0][1:]
    f.close()
    for i in t:
        ver = str(i[1][0][0])
        for j in i[1][0][1:]:
            ver = ver + '.' + str(j)
        print('app-emacs/' + i[0] + ' ' + ver)
    return 0

def list_categories(overlay):
    print('app-emacs')
    return 0

def package(overlay, pkg, ver, var):
    pass

def phase(overlay, pkg, ver, fnc):
    pass

def ebuild_function(cmd):
    pass

def main():
    args = sys.argv[1:]

    if args[0] == "GAPI":
        print("0")
        return 0
    
    if len(args) < 2:
        raise GElispError("Not enough arguments")
    overlay = args[0]
    cmd = args[1]
    
    if cmd == "sync":
        if len(args) < 3:
            url = None
        else:
            url = args[2]
        return sync(overlay, url)

    elif cmd == "list-packages":
        return list_packages(overlay)
    
    elif cmd == "list-categories":
        return list_categories(overlay)

    elif cmd == package:
        if len(args) < 4:
            raise GElispError("Not enough arguments")
        pkg = args[2][10:]
        ver = args[3]
        if len(args) < 5:
            var = None
        else:
            var = args[4]
        return package(overlay, pkg, ver, var)

    elif cmd == phase:
        if len(args) < 5:
            raise GElispError("Not enough arguments")
        pkg = args[2][10:]
        ver = args[3]
        fnc = args[4]
        return phase(overlay, pkg, ver, fnc)

    elif overlay == "ebuild":
        return ebuild_function(cmd)

    else:
        raise GElispError("Wrong arguments")


if __name__ == "__main__":
    sys.exit(main())