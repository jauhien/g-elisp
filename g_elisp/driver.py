#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from g_common.driver import Driver
from g_elisp.files import GELispOverlayConfig

class GELispDriver(Driver):
    def __init__(self):
        super().__init__()

    def sync(self, args):
        self.method = args.method
        o_cfg = GELispOverlayConfig(args.overlay)
        try:
            o_cfg.read()
        except IOError as e:
            pass
        o_cfg.cfg['overlay'] = {'method' : self.method}
        o_cfg.write()
        self.overlay = args.overlay
        self.name = os.path.split(args.overlay)[1]
        print('g-elisp: syncing overlay ' + self.name)
        return 0
