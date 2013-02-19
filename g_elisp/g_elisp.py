#!/usr/bin/python
# -*- coding: utf-8 -*-

from g_elisp.driver import GELispDriver

def main():
    g_driver = GELispDriver()
    return g_driver()

if __name__ == "__main__":
    sys.exit(main())
