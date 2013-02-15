#!/usr/bin/env python

from distutils.core import setup

from g_elisp.version import VERSION

setup(name          = 'g-elisp',
      version       = VERSION,
      description   = 'Driver for g-common repository of emacs packages',
      author        = 'Jauhien Piatlicki',
      author_email  = 'piatlicki@gmail.com',
      packages      = ['g_elisp'],
      scripts       = ['bin/g-elisp'],
      package_data  = {'g_elisp': ['data/*']},
      license       = 'GPL',
      )
