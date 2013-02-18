#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from g_common.driver import Driver

from g_elisp.files import GELispOverlayConfig, ArchiveContents, get_eclfile
from g_elisp.parsers import Package

class GELispDriver(Driver):
    def __init__(self):
        super().__init__()

    def sync(self, args):
        self.method = args.method
        self.uri = args.uri
        o_cfg = GELispOverlayConfig(args.overlay)
        try:
            o_cfg.read()
        except IOError as e:
            pass
        o_cfg.cfg['overlay'] = {'method' : self.method, 'uri' : self.uri}
        o_cfg.write()
        self.overlay = args.overlay
        self.name = os.path.split(args.overlay)[1]
        print('g-elisp: syncing overlay ' + self.name)
        o_arc = ArchiveContents(self.overlay)
        o_arc.sync(self.uri)
        return 0

    def eclass_list(self, args):
        print('g-elisp')
        return 0

    def eclass_src(self, args):
        with open(get_eclfile(), 'r') as eclass:
            print(eclass.read())
        return 0

    def ebuild_list(self, args):
        self.overlay = args.overlay
        o_arc = ArchiveContents(self.overlay)
        repo = o_arc.parse()
        for p in repo:
            print("app-emacs/" + p.name + " " + p.version)
        return 0

    def ebuild_src(self, args):
        self.overlay = args.overlay
        o_arc = ArchiveContents(self.overlay)
        repo = o_arc.parse()
        o_cfg = GELispOverlayConfig(self.overlay)
        o_cfg.read()
        print("""# Copyright 1999-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=5

inherit g-elisp

""")
        pkg = Package(args.name.split('/')[1], args.version)
        attr = repo[pkg]
        uri = o_cfg.cfg['overlay']['uri']
        print('DESCRIPTION="' + attr.desc + '"')
        print('HOMEPAGE="' + uri + '"')
        print('SRC_URI=""')
        print('LICENSE="GPL-2"')
        print()
        print('SLOT="0"')
        print('KEYWORDS="~amd64 ~x86"')
        print('IUSE=""')
        print('')
        print('REPO_URI="' + uri + '"')
        print('PKG_TYPE="' + attr.type + '"')
        print()
        deps = ""
        for i in attr.deps:
            deps += "\n\tapp-emacs/" + i.name + "-" + i.version
        print('DEPEND="${DEPEND}' + deps + '"')
        print('RDEPEND="${DEPEND}"')
        print()
        return 0
