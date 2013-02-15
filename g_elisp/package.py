#!/usr/bin/python
# -*- coding: utf-8 -*-

from g_elisp.parsers import parse_repo, parse_config
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

EBUILD_VARS = {"DESCRIPTION" : get_description,
               "HOMEPAGE" : get_homepage,
               "SRC_URI" : get_src_uri,
               "LICENSE" : get_license,
               "SLOT" : get_slot,
               "KEYWORDS" : get_keywords,
               "IUSE" : get_iuse,
               "REPO_URI" : get_repo_uri,
               "PKG_TYPE" : get_pkg_type}

