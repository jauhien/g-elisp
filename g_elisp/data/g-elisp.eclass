#
# @ECLASS: g-elisp.eclass
#
# @ECLASS-VARIABLE: REPO_URI
# @DEFAULT_UNSET
# @DESCRIPTION:
#
# @ECLASS-VARIABLE: PKG_TYPE
# @DEFAULT_UNSET
# @DESCRIPTION:
#
# @ECLASS-VARIABLE: REALNAME
# @DEFAULT_UNSET
# @DESCRIPTION:
#
# @ECLASS-VARIABLE: GELISP_STORE_DIR
# @DEFAULT_UNSET
# @DESCRIPTION:
GELISP_STORE_DIR="${PORTAGE_ACTUAL_DISTDIR:-${DISTDIR}}"
#
# @ECLASS-VARIABLE: GELISP_FETCH_CMD
# @DESCRIPTION:
# subversion update command
GELISP_FETCH_CMD="wget"

inherit elisp

EXPORT_FUNCTIONS src_{unpack,compile,install}

g-elisp_fetch() {
	addwrite "${GELISP_STORE_DIR}"
	pushd "${GELISP_STORE_DIR}" >/dev/null || die "can't chdir to ${GELISP_STORE_DIR}"
	if [[ ! -f "${P}.${PKG_TYPE}" ]]; then
		$GELISP_FETCH_CMD ${REPO_URI}/${REALNAME}-${PV}.${PKG_TYPE}
	fi
	cp ${REALNAME}-${PV}.${PKG_TYPE} ${DISTDIR}/${P}.${PKG_TYPE}
	popd >/dev/null
}

g-elisp_src_unpack() {
	g-elisp_fetch
	if [[ ${PKG_TYPE} != "el" ]]; then
		unpack ${P}.${PKG_TYPE}
	else
		cp ${DISTDIR}/${P}.${PKG_TYPE} .
	fi
	elisp_src_unpack
}

g-elisp_src_compile() {
	rm -f ${PN}-pkg.el
	elisp-make-autoload-file
	elisp_src_compile
}

g-elisp_src_install() {
	local sitefile="50${PN}-gentoo.el"
	cat <<EOF >> ${sitefile}
(add-to-list 'load-path "@SITELISP@")
(load "${PN}-autoloads" nil t)
EOF
	elisp-site-file-install ${sitefile}
	rm -f ${sitefile}
	elisp_src_install
}
