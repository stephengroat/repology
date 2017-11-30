# Copyright (C) 2017 Dmitry Marakasov <amdmi3@amdmi3.ru>
# Copyright (C) 2017 Felix Van der Jeugt <felix.vanderjeugt@gmail.com>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import os
import plistlib
import sys

from repology.package import Package
from repology.util import GetMaintainers


def SanitizeVersion(version):
    origversion = version

    version = version.split('_', 1)[0]

    if version != origversion:
        return version, origversion
    else:
        return version, None


class VoidLinuxParser():
    def __init__(self):
        pass

    def Parse(self, path):
        index_path = os.path.join(path, 'index.plist')
        plist_index = plistlib.load(open(index_path, 'rb'), fmt=plistlib.FMT_XML)

        packages = []
        for pkgname, props in plist_index.items():
            pkg = Package()

            if 'source-revisions' in props:
                pkg.effname = props['source-revisions'].split(':', 1)[0]
            else:
                print('WARNING: No source-revisions field for "{}"'.format(pkgname), file=sys.stderr)

            if not props['pkgver'].startswith(pkgname + '-'):
                print('WARNING: Bad pkgver for "{}"'.format(pkgname), file=sys.stderr)
                continue

            pkg.name = pkgname
            pkg.version, pkg.origversion = SanitizeVersion(props['pkgver'][len(pkgname) + 1:])
            pkg.maintainers = GetMaintainers(props.get('maintainer', ''))
            pkg.comment = props['short_desc']
            pkg.homepage = props['homepage']
            pkg.licenses = [l.strip() for l in props['license'].split(',')]

            packages.append(pkg)

        return packages
