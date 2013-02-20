#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

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
        except Exception:
            print ('Error when syncing')
            return -1 
        return 0
    
    def list_eclasses(self):
        return ['g-elisp']

    def get_eclass(self, eclass):
        ecl = TextFile(self.eclfile, os.path.join(get_pkgpath(), self.ecldir), self.datadir)
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
        attr = self.arc.sec[pkg]
        if self.uri is None:
            o_cfg = ConfigFile(self.cfgfile, datadir, datadir)
            o_cfg.cached_read()
            self.uri = o_cfg.src['overlay']['uri']
        deps = ""
        for i in attr.deps:
            deps += "\n\tapp-emacs/" + i.name.replace('.','_')
        ebuild_src = ["# Copyright 1999-2013 Gentoo Foundation",
                      "# Distributed under the terms of the GNU General Public License v2",
                      "# $Header: $",
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
                      'PKG_TYPE="' + attr.type + '"',
                      'PKG_TYPE="' + attr.type + '"',
                      "",
                      'DEPEND="${DEPEND}' + deps + '"',
                      'RDEPEND="${DEPEND}"'
                      ]
        return ebuild_src

## import os

## from g_common.driver import Driver

## from g_elisp.files import GELispOverlayConfig, ArchiveContents, get_eclfile
## from g_elisp.parsers import Package

## class GELispDriver(Driver):
##     def __init__(self):
##         super().__init__()

##     def sync(self, args):
##         self.method = args.method
##         self.uri = args.uri
##         o_cfg = GELispOverlayConfig(args.overlay)
##         try:
##             o_cfg.read()
##         except IOError as e:
##             pass
##         o_cfg.cfg['overlay'] = {'method' : self.method, 'uri' : self.uri}
##         o_cfg.write()
##         self.overlay = args.overlay
##         self.name = os.path.split(args.overlay)[1]
##         print('g-elisp: syncing overlay ' + self.name)
##         o_arc = ArchiveContents(self.overlay)
##         o_arc.sync(self.uri)
##         return 0

##     def eclass_list(self, args):
##         print('g-elisp')
##         return 0

##     def eclass_src(self, args):
##         with open(get_eclfile(), 'r') as eclass:
##             print(eclass.read())
##         return 0

##     def ebuild_list(self, args):
##         self.overlay = args.overlay
##         o_arc = ArchiveContents(self.overlay)
##         repo = o_arc.parse()
##         for p in repo:
##             print("app-emacs/" + p.name + " " + p.version)
##         return 0

##     def ebuild_src(self, args):
##         self.overlay = args.overlay
##         o_arc = ArchiveContents(self.overlay)
##         repo = o_arc.parse()
##         o_cfg = GELispOverlayConfig(self.overlay)
##         o_cfg.read()
##         print("""# Copyright 1999-2013 Gentoo Foundation
## # Distributed under the terms of the GNU General Public License v2
## # $Header: $

## EAPI=5

## inherit g-elisp

## """)
##         pkg = Package(args.name.split('/')[1], args.version)
##         attr = repo[pkg]
##         uri = o_cfg.cfg['overlay']['uri']
##         print('DESCRIPTION="' + attr.desc + '"')
##         print('HOMEPAGE="' + uri + '"')
##         print('SRC_URI=""')
##         print('LICENSE="GPL-2"')
##         print()
##         print('SLOT="0"')
##         print('KEYWORDS="~amd64 ~x86"')
##         print('IUSE=""')
##         print('')
##         print('REPO_URI="' + uri + '"')
##         print('PKG_TYPE="' + attr.type + '"')
##         print()
##         deps = ""
##         for i in attr.deps:
##             deps += "\n\tapp-emacs/" + i.name
##         print('DEPEND="${DEPEND}' + deps + '"')
##         print('RDEPEND="${DEPEND}"')
##         print()
##         return 0
