#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    brew install pandoc
fi
# pandoc is already installed by .travis.yml on Linux