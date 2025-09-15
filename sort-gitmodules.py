#!/usr/bin/env python3
#
# Code is released into public domain

from collections import defaultdict

sections = defaultdict(list)
section_name = ''

with open('.gitmodules', 'r') as f:
    for line in f:
        if line.startswith('['):
            section_name = line
        sections[section_name].append(line)

with open('.gitmodules', 'w') as f:
    for section_name in sorted(sections):
        f.write(''.join(sections[section_name]))

print('Sorted .gitmodules. Review output and commit.')
