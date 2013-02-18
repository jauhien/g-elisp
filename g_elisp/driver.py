#!/usr/bin/python
# -*- coding: utf-8 -*-

from g_common.driver import Driver

class GELispDriver(Driver):
    def __init__(self, overlay, method=None):
        super().__init__()
        self.method = method
        o_cfg = GELispOverlayConfig(overlay)
        if self.method is None:
            o_cfg.read()
            self.method = o_cfg.cfg['overlay']['method']
        else:
            try:
                o_cfg.read()
            except IOError as e:
                pass
            o_cfg.cfg['overlay'] = {'method' : self.method}
            o_cfg.write()
        self.overlay = overlay
        self.name = os.path.split(overlay)[1]

    def sync(self, args):
        print('g-elisp: syncing')
        return 0
