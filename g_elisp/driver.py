#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

import os

from pyparsing import ParseException

from g_common.overlay import Driver
from g_common.files import ConfigFile, TextFile

from g_elisp.files import ArchiveContents, get_pkgpath
from g_elisp.parsers import Package, Attributes

class GELispDriver(Driver):
    def __init__(self):
        super().__init__()
        self.datadir = ".g-elisp"
        self.arcfile = "archive-contents"
        self.cfgfile = "overlay.cfg"
        self.ecldir = "data"
        self.eclfile = "g-elisp.eclass"
        self.arc = None
        self.uri = None
    
    def sync(self, args):
        self.overlay = args.overlay
        self.method = args.method
        self.uri = args.uri
        datadir = os.path.join(self.overlay, self.datadir)
        o_cfg = ConfigFile(self.cfgfile, datadir, datadir)
        try:
            o_cfg.cached_read()
        except Exception:
            pass
        o_cfg.src['overlay'] = {'method' : self.method, 'uri' : self.uri}
        try:
            o_cfg.cached_write()
        except Exception:
            print ('Error when writing overlay config')
            return -1
        arc = ArchiveContents(self.arcfile, datadir, datadir)
        try:
            arc.sync(self.uri)
        except IOError as error:
            print('Error when syncing: ' + error.strerror)
            return -1
        except ParseException as error:
            print('Error when syncing: ' + str(error))
            return -1
        except Exception:
            print ('Error when syncing')
            return -1 
        return 0
    
    def list_eclasses(self):
        return ['g-elisp']

    def get_eclass(self, eclass):
        datadir = os.path.join(self.overlay, self.datadir)
        ecl = TextFile(self.eclfile, os.path.join(get_pkgpath(), self.ecldir), datadir)
        ecl.cached_read()
        return ecl.src

    def list_ebuilds(self):
        datadir = os.path.join(self.overlay, self.datadir)
        if self.arc is None:
            self.arc = ArchiveContents(self.arcfile, datadir, datadir)
            self.arc.cached_read()
        ebuilds = []
        for pkg in self.arc.src:
            ebuilds += [('app-emacs', pkg.name, pkg.version),]
        return ebuilds

    def get_ebuild(self, ebuild):
        print(ebuild)
        datadir = os.path.join(self.overlay, self.datadir)
        if self.arc is None:
            self.arc = ArchiveContents(self.arcfile, datadir, datadir)
            self.arc.cached_read()
        pkg = Package(ebuild[1], ebuild[2])
        attr = self.arc.src[pkg]
        if self.uri is None:
            o_cfg = ConfigFile(self.cfgfile, datadir, datadir)
            o_cfg.cached_read()
            self.uri = o_cfg.src['overlay']['uri']
        deps = ""
        for i in attr.deps:
            deps += "\n\tapp-emacs/" + i.name.replace('.','_')
        pkgtype = attr.type.replace('single', 'el')
        ebuild_src = ["# automatically generated by g-elisp"
                      "# please do not edit this file",
                      "",
                      "EAPI=5",
                      "",
                      "inherit g-elisp",
                      "",
                      'DESCRIPTION="' + attr.desc + '"',
                      'HOMEPAGE="' + self.uri + '"',
                      'SRC_URI=""',
                      'LICENSE="GPL-2"',
                      "",
                      'SLOT="0"',
                      'KEYWORDS="~amd64 ~x86"',
                      'IUSE=""',
                      "",
                      'REPO_URI="' + self.uri + '"',
                      'PKG_TYPE="' + pkgtype + '"',
                      'REALNAME="' + attr.realname + '"',
                      "",
                      'DEPEND="${DEPEND}' + deps + '"',
                      'RDEPEND="${DEPEND}"'
                      ]
        return ebuild_src
