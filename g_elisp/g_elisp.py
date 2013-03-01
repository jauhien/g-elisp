#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

from g_elisp.driver import GELispDriver

def main():
    g_driver = GELispDriver()
    return g_driver()

if __name__ == "__main__":
    sys.exit(main())
