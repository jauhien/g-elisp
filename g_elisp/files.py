#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from g_common.files import ConfigFile

DATADIR = ".g-elisp"
ARCFILE = "archive-contents"
CFGFILE = "overlay.cfg"
ECLFILE = "data/g-elisp.eclass"

class GELispOverlayConfig(ConfigFile):
    def __init__(self, overlay):
        super().__init__(os.path.join(overlay, DATADIR), CFGFILE)

def get_datadir(overlay):
    return os.path.join(overlay, DATADIR)

def get_arcfile(overlay):
    datadir = get_datadir(overlay)
    return os.path.join(datadir, ARCFILE)

def get_cfgfile(overlay):
    datadir = get_datadir(overlay)
    return os.path.join(datadir, CFGFILE)

def get_pkgpath():
    root = __file__
    if os.path.islink(root):
        root = os.path.realpath(root)
    return os.path.dirname(os.path.abspath(root))

def get_eclfile():
    path = get_pkgpath()
    return os.path.join(path, ECLFILE)

