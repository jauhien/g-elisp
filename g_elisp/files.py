#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from g_common.files import ConfigFile

from g_elisp.parsers import repo

DATADIR = ".g-elisp"
ARCFILE = "archive-contents"
CFGFILE = "overlay.cfg"
ECLFILE = "data/g-elisp.eclass"

class GELispOverlayConfig(ConfigFile):
    def __init__(self, overlay):
        super().__init__(os.path.join(overlay, DATADIR), CFGFILE)

class ArchiveContents:
    def __init__(self, overlay):
        self.name = ARCFILE
        self.directory = os.path.join(overlay, DATADIR)
        self.path = os.path.join(self.directory, ARCFILE)

    def sync(self, uri):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        archive_contents = urljoin(uri, 'archive-contents')
        h = request.urlopen(archive_contents)
        f = open(self.path, 'wb')
        f.write(h.read())
        h.close()
        f.close()
        return 0

    def parse(self):
        with open(self.path, 'r') as arcfile:
            self.repo = repo.parseFile(arcfile).asDict()
        return self.repo

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

