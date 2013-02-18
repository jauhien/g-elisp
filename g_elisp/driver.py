#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from g_common.driver import Driver

from g_elisp.files import GELispOverlayConfig, ArchiveContents, get_eclfile

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
        o_arc = ArchiveContents(self.overlay)
        repo = o_arc.parse()
        for p in repo:
            print("app-emacs/" + p.name + " " + p.version)
        return 0

    def ebuild_src(self, args):
        print("""# Copyright 1999-2012 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=5

SLOT="0"

DESCRIPTION="test"
HOMEPAGE="http://test.org"
SRC_URI=""
""")
        return 0
