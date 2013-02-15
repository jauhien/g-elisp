#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, collections, os
from urllib import request
from urllib.parse import urljoin

from g_elisp.files import get_datadir, get_arcfile, get_cfgfile, get_eclfile
from g_elisp.parsers import parse_repo, parse_args, parse_config, write_config, \
     Argument, Arguments, Command_group, Command
from g_elisp.package import EBUILD_VARS

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
    cfg = {"overlay": {"url" : url}}
    write_config(cfgfile, cfg)
    return 0

def list_categories(args):
    print('app-emacs')
    return 0

def list_packages(args):
    overlay = args.overlay[0]
    f = open(get_arcfile(overlay), 'r')
    package_dict = parse_repo(f).asDict()
    f.close()
    for name, attr in package_dict.items():
        print('app-emacs/' + name + ' ' + attr.version)
    return 0

def list_eclasses(args):
    print(g-elisp)
    return 0

def list_licenses(args):
    return 0

def get_EAPI(args):
    print(5)
    return 0

def get_inherit_list(args):
    print("g-elisp")
    return 0

def list_vars(args):
    for i in EBUILD_VARS:
        print(i)
    return 0

def get_vars(args):
    if args.var is None:
        for i in EBUILD_VARS:
            print(i + "=" + '"' + EBUILD_VARS[i](args.overlay, args.package_name) + '"')
    else:
        print(args.var + "=" + '"' + EBUILD_VARS[args.var](args.overlay, args.package_name) + '"')
    return 0

def list_phases(args):
    return 0

def get_phase(args):
    return 0

def get_eclass(args):
    eclass = open(get_eclfile(), 'r')
    print(eclass.read())
    eclass.close()
    return 0

def get_license(args):
    return 0

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
