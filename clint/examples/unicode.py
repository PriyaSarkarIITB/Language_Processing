#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs

sys.path.insert(0, os.path.abspath('..'))

try:
    import json
except:
    import simplejson as json

from clint.arguments import Args
from clint import piped_in
from clint.textui import colored, puts, indent

args = Args()

if __name__ == '__main__':

    puts('Test:')
    with indent(4):
        puts('%s Fake test 1.' % colored.green('✔'))
        puts('%s Fake test 2.' % colored.red('✖'))

    puts('')
    puts('Greet:')
    with indent(4):
        puts(colored.red('Здравствуйте'))
        puts(colored.green('你好。'))
        puts(colored.yellow('سلام'))
        puts(colored.magenta('안녕하세요'))
        puts(colored.blue('नमस्ते'))
        puts(colored.cyan('γειά σου'))

    puts('')
    puts('Arguments:')
    with indent(4):
        puts('%s' % colored.red(args[0]))

    puts('')
    puts('File:')
    with indent(4):
        f = args.files[0]
        puts(colored.yellow('%s:' % f))
        with indent(2):
            fd = codecs.open(f, encoding='utf-8')
            for line in fd:
                line = line.strip('\n\r')
                puts(colored.yellow('  %s' % line))
            fd.close()

    puts('')
    puts('Input:')
    with indent(4):
        in_data = json.loads(piped_in())
        title = in_data['title']
        text = in_data['text']
        puts(colored.blue('Title: %s' % title))
        puts(colored.magenta('Text: %s' % text))
