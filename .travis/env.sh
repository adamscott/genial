#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    alias gnu_readlink=greadlink

else # Linux
    alias gnu_readlink=readlink
fi

# Sets $PATH to access generated static-qt binaries
export PATH="$(gnu_readlink -f .)/pyqtdeploy/qt-5.7.0/bin":$PATH
