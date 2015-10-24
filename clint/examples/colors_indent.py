#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement


import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import puts, indent, colored

lorem = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'

if __name__ == '__main__':
    puts('This is an example of text that is not indented. Awesome, eh?')
    puts('Lets quote some text.')
    with indent(4, quote=colored.blue('.')):
        puts('This is indented text.')
        with indent(3, quote=colored.blue(' >')):
            puts('This is quoted text.')
            puts(colored.green(lorem))
        puts("And, we're back to the previous index level. That was easy.")
        
        with indent(12, quote=colored.cyan(' |')):
            puts('This is massively indented text.')
            puts(colored.magenta('This is massively indented text that\'s colored'))
            puts("Now I'll show you how to negatively indent.")
            
            with indent(-5, quote=colored.yellow('!! ')):
                puts('NOTE: ' + colored.red('INCEPTION!'))
                
            puts('And back to where we were.')
        puts('Back to level 1.')
    puts('Back to normal.')