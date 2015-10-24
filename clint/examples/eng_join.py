#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.eng import join
from clint.textui import colored, indent, puts

colors = [
    colored.blue('blue'),
    colored.red('red'),
    colored.yellow('yellow'),
    colored.green('green'),
    colored.magenta('magenta')
]

colors = [str(cs) for cs in colors]


puts('Smart:')
with indent(4):
    for i in range(len(colors)):
        puts(join(colors[:i+1]))
puts('\n')
puts('Stupid:')
with indent(4):
    for i in range(len(colors)):
        puts(join(colors[:i+1], im_a_moron=True, conj='\'n'))
