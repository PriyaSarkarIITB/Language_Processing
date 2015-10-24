#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import colored

text = 'THIS TEXT IS COLORED %s!'

if __name__ == '__main__':

	for color in colored.COLORS:
		print(getattr(colored, color)(text % color.upper()))
