# Copyright (C) 2017 Dmitry Marakasov <amdmi3@amdmi3.ru>
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

import sys


from repology.package import Package


class FourMAddonsTxtParser():
    def __init__(self):
        pass

    def Parse(self, path):
        result = []

        with open(path, encoding='utf-8') as addonsfile:
            for line in addonsfile:
                line = line.strip()

                if line.startswith('addon_') and line.endswith('.tar.xz'):
                    pkg = Package()

                    try:
                        pkg.name, pkg.version = line[6:-7].rsplit('-', 1)
                        result.append(pkg)
                    except:
                        print('WARNING: unable to parse line: {}'.format(line), file=sys.stderr)
                        pass

        return result
