#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    brew upgrade pyenv
fi
# pyenv is already installed in the Linux container

eval "$(pyenv init -)"
pyenv install 3.5.2
pyenv global 3.5.2

pip install --upgrade pip
pip install --upgrade setuptools
