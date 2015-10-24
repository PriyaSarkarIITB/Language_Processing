#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import puts, indent

lorem = '''
Lorem ipsum dolor sit amet, consectetur adipisicing elit
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in 
culpa qui officia deserunt mollit anim id est laborum.
    '''

if __name__ == '__main__':
    with indent(4):
        puts(lorem)
        
    with indent(5, quote=' |'):
        with open('newline_indent.py', 'r') as f:
            puts(f.read())