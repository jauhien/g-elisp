#!/usr/bin/python
# -*- coding: utf-8 -*-

from g_common.parsers import parse_config

from g_elisp.parsers import parse_repo
from g_elisp.files import get_arcfile, get_cfgfile

def get_description(overlay, pkg_name):
    f = open(get_arcfile(overlay), 'r')
    package_dict = parse_repo(f).asDict()
    f.close()
    attr = package_dict[pkg_name]
    return attr.desc

def get_homepage(overlay, pkg_name):
    f = get_cfgfile(overlay)
    cfg = parse_config(f)
    homepage = cfg['overlay']['url']
    return homepage

def get_src_uri(overlay, pkg_name):
    return ""

def get_license(overlay, pkg_name):
    return "GPL-2"

def get_slot(overlay, pkg_name):
    return "0"

def get_keywords(overlay, pkg_name):
    return "~amd64 ~x86"

def get_iuse(overlay, pkg_name):
    return ""

def get_repo_uri(overlay, pkg_name):
    return get_homepage(overlay, pkg_name)

def get_pkg_type(overlay, pkg_name):
    f = open(get_arcfile(overlay), 'r')
    package_dict = parse_repo(f).asDict()
    f.close()
    attr = package_dict[pkg_name]
    return attr.type

def get_depend(overlay, pkg_name):
    depend = "${DEPEND}"
    f = open(get_arcfile(overlay), 'r')
    package_dict = parse_repo(f).asDict()
    f.close()
    deps = package_dict[pkg_name].deps
    for i in deps:
        depend += "\n\tapp-emacs/" + i.name + "-" + i.version
    return depend

def get_rdepend(overlay, pkg_name):
    return("${DEPEND}")

EBUILD_VARS_DICT = {"DESCRIPTION" : get_description,
               "HOMEPAGE" : get_homepage,
               "SRC_URI" : get_src_uri,
               "LICENSE" : get_license,
               "SLOT" : get_slot,
               "KEYWORDS" : get_keywords,
               "IUSE" : get_iuse,
               "REPO_URI" : get_repo_uri,
               "PKG_TYPE" : get_pkg_type,
               "DEPEND" : get_depend,
               "RDEPEND" : get_rdepend}

EBUILD_VARS_LIST = ["DESCRIPTION",
               "HOMEPAGE",
               "SRC_URI",
               "LICENSE",
               "SLOT",
               "KEYWORDS",
               "IUSE",
               "REPO_URI",
               "PKG_TYPE",
               "DEPEND",
               "RDEPEND"]
