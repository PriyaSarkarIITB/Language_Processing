#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import prompt, puts, colored, validators

if __name__ == '__main__':
    # Standard non-empty input
    name = prompt.query("What's your name?")

    # Set validators to an empty list for an optional input
    language = prompt.query("Your favorite tool (optional)?", validators=[])

    # Use a default value and a validator
    path = prompt.query('Installation Path', default='/usr/local/bin/', validators=[validators.PathValidator()])

    puts(colored.blue('Hi {0}. Install {1} to {2}'.format(name, language or 'nothing', path)))
