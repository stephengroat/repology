#
# Custom describe target for advanced FreeBSD ports parsing
#
# Example usage:
#
#     env __MAKE_CONF=`pwd`/describe.mk INDEX_TMPDIR=`pwd` INDEXDIR=`pwd` make -C /usr/ports index
#
.if ${.CURDIR:H:H:T} == "ports"

.if !defied(INDEX_OUT)
INDEX_OUT=	/dev/stdout
.endif

# Package name
# Package version
# Comment
# Maintainer
# Categories
# Licenses
# LICENSE_COMB
# Downloads
# WWW

describe:
	@( \
		${ECHO_CMD} -n "${PKGNAMEPREFIX}${PORTNAME}${PKGNAMESUFFIX}|"; \
		${ECHO_CMD} -n "${PORTVERSION:C/[-_,]/./g}|"; \
		${ECHO_CMD} -n ${COMMENT:Q}"|"; \
		${ECHO_CMD} -n "${MAINTAINER}|"; \
		${ECHO_CMD} -n "${CATEGORIES}|"; \
		${ECHO_CMD} -n "${LICENSE}|"; \
		${ECHO_CMD} -n "${LICENSE_COMB}|"; \
		${SETENV} DISTDIR=/tmp/empty MASTER_SITE_BACKUP= ${MAKE} fetch-url-list | ${TR} '\n' ' ' | ${SED} -e 's| $$||' | ${TR} -d '\n'; \
		${ECHO_CMD} -n "|"; \
		while read one two discard; do \
			case "$$one" in \
			WWW:)   case "$$two" in \
				https://*|http://*|ftp://*) ${ECHO_CMD} -n "$$two" ;; \
				*) ${ECHO_CMD} -n "http://$$two" ;; \
				esac; \
				break; \
				;; \
			esac; \
		done < ${DESCR}; \
		${ECHO_CMD} \
	) >>${INDEX_OUT}
.endif
