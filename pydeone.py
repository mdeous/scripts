#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#TODO: add ability to post on user account

__app__ = 'pydeone'
__version__ = '0.3'
__author__ = 'MatToufoutu'


from optparse import OptionParser
from os import getcwd, path
from socket import setdefaulttimeout, timeout
from sys import exit as sysexit
from sys import stdin
from urllib import urlencode
from urllib2 import urlopen


def getopts():
    usage = '%prog [options]'
    opts = OptionParser(usage=usage, version=__version__)
    opts.add_option('-f', '--file', dest='file', default='stdin',
                    help="source file to paste (default: stdin)")
    opts.add_option('-l', '--lang', dest='lang', default='text',
                    help="programming language (default: text)")
    opts.add_option('-i', '--in', dest='input', default = '',
                    help="input data (works only if --run is used)")
    opts.add_option('-n', '--note', dest='note', default='',
                    help="optional note to attach to paste")
    opts.add_option('-s', '--show-langs', action='store_true', default=False, dest='show',
                    help="display available languages")
    opts.add_option('-r', '--run', action='store_true', default=False, dest='run',
                    help="run pasted code on ideone")
    opts.add_option('-p', '--private', action='store_true', default=False, dest='private',
                    help="do not display the code in 'recent pastes'")
    (options, args) = opts.parse_args()
    if options.show:
        for lang in sorted(LANGS.keys()):
            print lang
        sysexit(0)
    if args:
        print('Unrecognized argument(s): %s\n' % ', '.join(args))
        sysexit(1)
    if options.lang not in LANGS.keys():
        print('Unknown language, use --show-langs to display available languages\n')
        sysexit(1)
    return options

URL = 'http://www.ideone.com/ideone/index/submit/'
LANGS = {'ada': 7, 'assembler': 13, 'awk': 104, 'bash': 28, 'bc': 110, 'brainf**k': 12,
         'c': 11, 'c#': 27, 'c++': 1, 'c99': 34, 'clips': 14, 'clojure': 111, 'cobol': 106,
         'common': 32, 'd': 102, 'erlang': 36, 'forth': 107, 'fortran': 5, 'go': 114,
         'haskell': 21, 'icon': 16, 'intercal': 9, 'java': 10, 'javascript': 35, 'lua': 26,
         'nemerle': 30, 'nice': 25, 'ocaml': 8, 'pascal': 22, 'perl': 3, 'php': 29, 'pike': 19,
         'prolog': 108, 'python': 4, 'python3': 116, 'ruby': 17, 'scala': 39, 'scheme': 33,
         'smalltalk': 23, 'tcl': 38, 'text': 62, 'unlambda': 115, 'visual': 101, 'whitespace': 6}

options = getopts()
if (options.file == 'stdin') and not path.exists(path.join(getcwd(), 'stdin')):
    source = stdin.read()
else:
    if not path.exists(options.file):
        print("File not found: %s" % options.file)
        sysexit(1)
    source = open(options.file).read()

setdefaulttimeout(5)
lang = LANGS[options.lang]
run = 1 if options.run else 0
private = 1 if options.private else 0
POST = urlencode({'lang':lang, 'file':source, 'run':run, 'private':private,
                  'Submit':'submit', 'input':options.input, 'note':options.note})
try:
    webpage = urlopen(URL, POST)
    print(webpage.url)
    sysexit(0)
except timeout:
    print("Connection timed out")
    sysexit(2)
