# -*- coding: utf8 -*-

"""
clint.textui.prompt
~~~~~~~~~~~~~~~~~~~

Module for simple interactive prompts handling

"""

from __future__ import absolute_import, print_function

from re import match, I

from .core import puts
from .colored import yellow
from .validators import RegexValidator

try:
    raw_input
except NameError:
    raw_input = input


def yn(prompt, default='y', batch=False):
    # A sanity check against default value
    # If not y/n then y is assumed
    if default not in ['y', 'n']:
        default = 'y'

    # Let's build the prompt
    choicebox = '[Y/n]' if default == 'y' else '[y/N]'
    prompt = prompt + ' ' + choicebox + ' '

    # If input is not a yes/no variant or empty
    # keep asking
    while True:
        # If batch option is True then auto reply
        # with default input
        if not batch:
            input = raw_input(prompt).strip()
        else:
            print(prompt)
            input = ''

        # If input is empty default choice is assumed
        # so we return True
        if input == '':
            return True

        # Given 'yes' as input if default choice is y
        # then return True, False otherwise
        if match('y(?:es)?', input, I):
            return True if default == 'y' else False

        # Given 'no' as input if default choice is n
        # then return True, False otherwise
        elif match('n(?:o)?', input, I):
            return True if default == 'n' else False


def query(prompt, default='', validators=None, batch=False):
    # Set the nonempty validator as default
    if validators is None:
        validators = [RegexValidator(r'.+')]

    # Let's build the prompt
    if prompt[-1] is not ' ':
        prompt += ' '

    if default:
        prompt += '[' + default + '] '

    # If input is not valid keep asking
    while True:
        # If batch option is True then auto reply
        # with default input
        if not batch:
            user_input = raw_input(prompt).strip() or default
        else:
            print(prompt)
            user_input = ''

        # Validate the user input
        try:
            for validator in validators:
                user_input = validator(user_input)
            return user_input
        except Exception as e:
            puts(yellow(e.message))
