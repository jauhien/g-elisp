#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

DATADIR = ".g-elisp"
ARCFILE = "archive-contents"
CFGFILE = "overlay.cfg"

def get_datadir(overlay):
    return os.path.join(overlay, DATADIR)

def get_arcfile(overlay):
    datadir = get_datadir(overlay)
    return os.path.join(datadir, ARCFILE)

def get_cfgfile(overlay):
    datadir = get_datadir(overlay)
    return os.path.join(datadir, CFGFILE)
