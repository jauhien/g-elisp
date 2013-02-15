#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, collections, os
from urllib import request
from urllib.parse import urljoin

from g_elisp.files import get_datadir, get_arcfile, get_cfgfile
from g_elisp.parsers import parse_repo, parse_args, Argument, Arguments, Command_group, Command

def get_GAPI(args):
    print(0)
    return 0

def sync(args):
    overlay = args.overlay[0]
    url = args.url[0]
    datadir = get_datadir(overlay)
    if not os.path.exists(datadir):
        os.makedirs(datadir)
        
    arcfile = get_arcfile(overlay)
    archive_contents = urljoin(url, 'archive-contents')
    h = request.urlopen(archive_contents)
    f = open(arcfile, 'wb')
    f.write(h.read())
    h.close()
    f.close()

    cfgfile = get_cfgfile(overlay)
    f = open(cfgfile, 'wb')
    f.write(bytes("url = " + url, 'UTF-8'))
    f.close()
    return 0

def list_categories(args):
    print('app-emacs')
    return 0

def list_packages(args):
    overlay = args.overlay[0]
    f = open(get_arcfile(overlay), 'r')
    package_list = parse_repo(f)
    f.close()
    for p in package_list:
        print('app-emacs/' + p.name + ' ' + p.version)
    return 0

def list_eclasses(args):
    print(g-elisp)
    return 0

def list_licenses(args):
    pass

def get_EAPI(args):
    print(4)
    return 0

def get_inherit_list(args):
    pass

def list_vars(args):
    pass

def get_vars(args):
    pass

def list_phases(args):
    pass

def get_phase(args):
    pass

def get_eclass(args):
    
    return 0

def get_license(args):
    pass

def main():
    args = Arguments([Argument('overlay', 1)],
                     [Command('GAPI', 'display API version', [], get_GAPI),
                      Command('sync', 'sync overlay', [Argument('url', 1)], sync),
                      Command('list-categories', 'list categories', [], list_categories),
                      Command('list-packages', 'list packages', [], list_packages),
                      Command('list-eclasses', 'list eclasses', [], list_eclasses),
                      Command('list-licenses', 'list licenses', [], list_licenses),
                      Command_group('package', 'info for specific package',
                                    [Argument('package_name', 1),
                                     Argument('version', 1)],
                                    [Command('EAPI', 'display EAPI', [], get_EAPI),
                                     Command('inherit', 'display inherit list', [], get_inherit_list),
                                     Command('list-vars', 'list vars', [], list_vars),
                                     Command('vars', 'value of variables', [Argument('var', '?')], get_vars),
                                     Command('list-phases', 'list phases', [], list_phases),
                                     Command('phase', 'get phase source', [Argument('phase', 1)], get_phase),
                                     ]),
                      Command('eclass', 'eclass', [Argument('eclass', 1)], get_eclass),
                      Command('license', 'license', [Argument('license', 1)], get_license),
                      ])
    args = parse_args(args)
    return args.func(args)
    
if __name__ == "__main__":
    sys.exit(main())
