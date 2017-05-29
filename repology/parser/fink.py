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

import lxml.html

from repology.package import Package


def SanitizeVersion(version):
    origversion = version

    pos = version.rfind('-')
    if pos != -1:
        version = version[:pos]

    pos = version.find('+')
    if pos != -1:
        version = version[:pos]

    if version != origversion:
        return version, origversion
    else:
        return version, None


class FinkHTMLParser():
    def __init__(self):
        pass

    def Parse(self, path):
        result = []

        for row in lxml.html.parse(path).getroot().xpath('.//table[@class="pdb"]')[0].xpath('./tr[@class="package"]'):
            pkg = Package()

            pkg.name = row.xpath('./td[1]/a')[0].text
            pkg.version, pkg.origversion = SanitizeVersion(row.xpath('./td[2]')[0].text)
            pkg.comment = row.xpath('./td[3]')[0].text

            result.append(pkg)

        return result
