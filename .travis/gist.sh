#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OSX
    # install gist package
    brew install gist
fi
# gist is already installed by .travis.yml on Linux

# write gist token to ~/.gist
pushd ~
python -c """
import os
with open('.gist', 'w') as f:
    f.write(os.environ['GITHUB_GIST_TOKEN'])
"""
popd # ~
