#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import puts, colored
from clint.textui import columns

lorem = 'Lorem ipsum dolor sit amet, consehdfhdfhdfhdfhdfhctetur adi pisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

if __name__ == '__main__':
    # puts(min_width('test\nit', 20) + ' me')
    # puts(max_width(lorem, 20) + ' me')
    
    # print max_width(lorem, 45)
    
    col = 60
    
    puts(columns([(colored.red('Column 1')), col], [(colored.green('Column Two')), None],
                    [(colored.magenta('Column III')), col]))
    puts(columns(['hi there my name is kenneth and this is a columns', col], [lorem, None], ['kenneths', col]))
