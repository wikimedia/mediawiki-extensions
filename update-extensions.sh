#!/bin/sh

# Config
basePath="mediawiki/extensions/"

# Script to clone any missing extensions and updates the others
ssh -p 29418 gerrit.wikimedia.org gerrit ls-projects | grep "^${basePath}" | sed "s,${basePath},," | while read PROJECT
do
	echo "[${PROJECT}]:"
	# Clone projects that don't exist here...
	if [ ! -d "${PROJECT}" ]; then
		git clone "ssh://gerrit.wikimedia.org:29418/${basePath}${PROJECT}.git" "${PROJECT}"
	# Update any existing project...
	else
		cd "${PROJECT}"
		git pull
		cd "../"
	fi
done
