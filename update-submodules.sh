#!/bin/sh

# Config
basePath="mediawiki/extensions/"

# Script to add any missing submodules and update them to HEAD
ssh -p 29418 gerrit.wikimedia.org gerrit ls-projects | grep "^${basePath}" | sed "s,${basePath},," | while read PROJECT
do
	[ ! -d "${PROJECT}" ] && git submodule --quiet add "ssh://gerrit.wikimedia.org:29418/${basePath}${PROJECT}.git" "${PROJECT}"
done
