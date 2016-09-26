#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    brew uninstall pyenv # uninstall outdated pyenv
fi

# Unified pyenv install
wget -qO- https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    export PATH="/Users/travis/.pyenv/bin:$PATH"
else # Linux
    export PATH="/home/travis/.pyenv/bin:$PATH"
fi

eval "$(pyenv init -)"
pyenv install 3.5.2
pyenv global 3.5.2

pip install --upgrade pip
pip install --upgrade setuptools
