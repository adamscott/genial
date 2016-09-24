#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    brew update

else # Linux
    sudo apt-add-repository ppa:beineri/opt-qt57-trusty -y
    sudo apt-get update
fi
