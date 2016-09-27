#!/usr/bin/env bash
set -e

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    brew update

    brew install autoconf openssl readline xz  # pyenv dependencies
    brew install pandoc  # needed to convert .md to .rst
fi
# No need to setup packages in Linux build
