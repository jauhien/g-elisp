#!/usr/bin/env python
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

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
      data_files    = [('/usr/share/g-common/drivers/', ['elpa.cfg']),
                       ('/etc/layman/overlays/', ['elpa-overlays.xml']),],
      license       = 'GPL',
      )
