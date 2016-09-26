#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    brew uninstall pyenv # uninstall outdated pyenv
fi

# Unified pyenv install
wget -qO- https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

# Add ~/.pyenv to $PATH
if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    export PATH="/Users/travis/.pyenv/bin:$PATH"
else # Linux
    export PATH="/home/travis/.pyenv/bin:$PATH"
fi

# Makes builds a little faster
export PYTHON_CFLAGS='-O2'

# Inits pyenv
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Installs and sets global python to v3.5.2
pyenv install --verbose 3.5.2
pyenv global 3.5.2

# Get the latest version of pip and setuptools, which both come preinstalled, but outdated
pip install --upgrade pip
pip install --upgrade setuptools
