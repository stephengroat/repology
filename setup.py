#!/usr/bin/env python3

from distutils.core import setup, Extension
import subprocess

def pkgconfig(package):
    result = {}
    for token in subprocess.check_output(["pkg-config", "--libs" , "--cflags", package]).decode('utf-8').split():
        if token.startswith('-I'):
            result.setdefault('include_dirs', []).append(token[2:])
        elif token.startswith('-L'):
            result.setdefault('library_dirs', []).append(token[2:])
        elif token.startswith('-l'):
            result.setdefault('libraries', []).append(token[2:])
    return result

setup(
    name='repology',
    version='0.0.0',
    description='Compare package versions in many repositories',
    author='Dmitry Marakasov',
    author_email='amdmi3@amdmi3.ru',
    url='http://repology.org/',
    packages=[
        'repology',
        'repology.fetcher',
        'repology.parser',
    ],
    classifiers=[
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Software Distribution',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: C',
    ],
    ext_modules = [
        Extension(
            'repology.parser.helpers.rpm',
            sources=['repology/parser/helpers/rpm.c'],
            **pkgconfig('rpm')
        )
    ]
)
