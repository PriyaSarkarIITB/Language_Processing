#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint import piped_in
from clint.textui import colored, indent, puts


if __name__ == '__main__':
    in_data = piped_in()
    
    with indent(4, quote='>>>'):
        
        if in_data:
        
            puts('Data was piped in! Here it is:')
            with indent(5, quote=colored.red(' |')):
                puts(in_data)
        else:
            puts(colored.red('Warning: ') + 'No data was piped in.')
