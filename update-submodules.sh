#!/bin/bash

# Config
basePath="mediawiki/extensions/"

# Script to add any missing submodules and update them to HEAD
for p in `ssh -p 29418 gerrit.wikimedia.org gerrit ls-projects`
do
	if [[ $p = $basePath* ]]; then
		ext=${p:${#basePath}}
		if grep -v $ext .gitmodules; then
			`git submodule --quiet add ssh://gerrit.wikimedia.org:29418/$basePath$ext.git $ext`
		fi
	fi
done
