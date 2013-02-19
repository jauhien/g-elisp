#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from urllib import request
from urllib.parse import urljoin

from g_common.files import File

from g_elisp.parsers import repo, Package, Attributes

class ArchiveContents(File):
    def __init__(self, name, directory, cachedir):
        super().__init__(name, directory, cachedir)
        self.src = {}
        
    def _read_src(self):
        rp = repo.parseFile(self.path).asDict()
        self.src = {}
        for pkg, attr in rp.items():
            self.src[Package(pkg.name.replace('.','_'), pkg.version)] = \
                                                        Attributes(pkg.name, attr.deps, attr.desc, attr.type)

    def _write_src(self):
        with open(self.path, 'w') as f:
            f.write('(1 ')
            for pkg, attr in self.src.items():
                deps = []
                for dep in attr.deps:
                    deps += ['(' + dep.name + '('] + dep.version.split('.') + [')', ')']
                f.write(" ".join(['(', pkg.name, '. [('] + \
                                 pkg.version.split('.') + \
                                 [')', '('] + \
                                 deps + \
                                 [')', ''.join(['"', attr.desc, '"']),
                                  attr.type, '] )']
                                 ))
            f.write(')')
                
    def sync(self, uri):
        uri = urljoin(uri, 'archive-contents')
        h = request.urlopen(uri)
        with open(self.path, 'wb') as f:
            f.write(h.read())
        h.close()
        self.cached_read()
        

## import os
## from urllib import request
## from urllib.parse import urljoin

## from g_common.files import ConfigFile

## from g_elisp.parsers import repo

## DATADIR = ".g-elisp"
## ARCFILE = "archive-contents"
## CFGFILE = "overlay.cfg"
## ECLFILE = "data/g-elisp.eclass"

## class GELispOverlayConfig(ConfigFile):
##     def __init__(self, overlay):
##         super().__init__(os.path.join(overlay, DATADIR), CFGFILE)

## class ArchiveContents:
##     def __init__(self, overlay):
##         self.name = ARCFILE
##         self.directory = os.path.join(overlay, DATADIR)
##         self.path = os.path.join(self.directory, ARCFILE)

##     def sync(self, uri):
##         if not os.path.exists(self.directory):
##             os.makedirs(self.directory)
##         archive_contents = urljoin(uri, 'archive-contents')
##         h = request.urlopen(archive_contents)
##         f = open(self.path, 'wb')
##         f.write(h.read())
##         h.close()
##         f.close()
##         return 0

##     def parse(self):
##         with open(self.path, 'r') as arcfile:
##             self.repo = repo.parseFile(arcfile).asDict()
##         return self.repo


def get_pkgpath():
     root = __file__
     if os.path.islink(root):
         root = os.path.realpath(root)
     return os.path.dirname(os.path.abspath(root))
