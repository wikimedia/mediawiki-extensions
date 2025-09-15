#!/usr/bin/env python3
#
# Script to verify extensions entry point and report empty ones.
#
# Usage:
#
#   cd mediawiki/extensions
#   python check-entry-points.py
#
# Authors:
#  - Antoine "hashar" Musso, 2014
#  - Wikimedia Foundation Inc, 2014

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Files which are often added straight after an extension repository has been
# created.  If we only have some of them, that means the repository can be
# considered empty.
DEFAULT_FILES = ['.git', '.gitignore', '.gitreview']


for extension in sorted(os.listdir(BASE_DIR)):

    ext_dir = os.path.join(BASE_DIR, extension)

    if (extension == '.git' or os.path.isfile(ext_dir)):
        continue

    # Known entry points (ep):
    ep_php = os.path.join(BASE_DIR, extension, extension + ".php")
    has_php = os.path.exists(ep_php)
    ep_json = os.path.join(BASE_DIR, extension, 'extension.json')
    has_json = os.path.exists(ep_json)

    if has_json:
        continue

    if not has_php:
        dir_items = os.listdir(ext_dir)
        cwd = os.getcwd()
        if set(dir_items) - set(DEFAULT_FILES):
            print('Missing entry point: {}'
                  .format(os.path.relpath(ep_php, cwd)))
        else:
            print('Empty repository: {}'.format(os.path.relpath(ext_dir, cwd)))
