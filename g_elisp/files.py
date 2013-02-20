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

def get_pkgpath():
     root = __file__
     if os.path.islink(root):
         root = os.path.realpath(root)
     return os.path.dirname(os.path.abspath(root))
