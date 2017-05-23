# Copyright (C) 2016 Dmitry Marakasov <amdmi3@amdmi3.ru>
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
import lxml.etree

from repology.package import Package


class DistrowatchPackagesParser():
    def __init__(self):
        pass

    def Parse(self, path):
        result = []

        table = lxml.html.parse(path).getroot().xpath('.//table[@class="Auto"]')

        first = True
        for row in lxml.html.parse(path).getroot().xpath('.//table[@class="Auto"]')[0].xpath('./tr'):
            if first:
                first = False
                continue

            pkg = Package()

            # name + version
            cell = row.xpath('./th[1]/a[@href]')[0]
            pkg.name = cell.text
            pkg.homepage = cell.attrib['href']

            # summary
            cell = row.xpath('./td[1]/a')[0]
            pkg.version = cell.text
            pkg.downloads = [ cell.attrib['href'] ]

            # summary
            cell = row.xpath('./td[2]')[0]
            pkg.comment = cell.text

            result.append(pkg)

        return result