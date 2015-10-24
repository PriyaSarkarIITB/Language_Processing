#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.arguments import Args 
from clint.textui import puts, colored, indent

args = Args()

with indent(4, quote='>>>'):
    puts(colored.red('Aruments passed in: ') + str(args.all))
    puts(colored.red('Flags detected: ') + str(args.flags))
    puts(colored.red('Files detected: ') + str(args.files))
    puts(colored.red('NOT Files detected: ') + str(args.not_files))
    puts(colored.red('Grouped Arguments: ') + str(dict(args.grouped)))
    
print 

