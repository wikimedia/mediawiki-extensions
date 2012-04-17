#!/bin/sh

# Config
basePath="mediawiki/extensions/"

# Check for git-review
if [ -z $(which git-review) ]; then
	echo "git-review not detected. Aborting."
	exit 1
fi

# Script to clone any missing extensions and updates the others
ssh -p 29418 gerrit.wikimedia.org gerrit ls-projects | grep "^${basePath}" | sed "s,${basePath},," | while read PROJECT
do
	echo "[${PROJECT}]:"
	# Clone projects that don't exist here...
	if [ ! -d "${PROJECT}" ]; then
		git clone "ssh://gerrit.wikimedia.org:29418/${basePath}${PROJECT}.git" "${PROJECT}"
		git-review -s
	# Update any existing project...
	else
		cd "${PROJECT}"
		git pull
		cd "../"
	fi
done
