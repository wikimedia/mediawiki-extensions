#!/bin/bash

echo "Refreshing remote"
git pull
echo "Refreshing submodules"
git submodule update --init --recursive

echo "Comparing HEAD and origin/master of each repository..."
echo "------------------------------------------------------"
git submodule --quiet foreach 'test "$(git rev-list HEAD..origin/master --count)" = "0" || echo "ERROR! $path is lagging behind."'
echo "------------------------------------------------------"

echo "Done! Any 'ERROR!' above this line should be reported in phabricator"
