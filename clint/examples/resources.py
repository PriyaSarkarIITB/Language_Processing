#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint import resources

resources.init('kennethreitz', 'clint')

lorem = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'


print('%s created.' % resources.user.path)

resources.user.write('lorem.txt', lorem)
print('lorem.txt created')

assert resources.user.read('lorem.txt') == lorem
print('lorem.txt has correct contents')

resources.user.delete('lorem.txt')
print('lorem.txt deleted')

assert resources.user.read('lorem.txt') == None
print('lorem.txt deletion confirmed')
