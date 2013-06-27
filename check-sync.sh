#!/bin/bash

echo "Refreshing remote"
git pull
echo "Refreshing submodules"
git submodule update --init

echo "Still there? Check each modules is up to date"
git submodule --quiet foreach 'test "$(git rev-list HEAD..origin/master --count)" = "0" || echo "ERROR! $path is lagging behind."'

echo "Done! Any ERROR! up this line should be reported in bugzilla"
