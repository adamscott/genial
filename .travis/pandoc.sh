#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    brew install pandoc

else # Linux
    $(: Do nothing) # Pandoc is installed by .travis.yml
fi
