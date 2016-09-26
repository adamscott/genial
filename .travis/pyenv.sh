#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OS X
    $(: do nothing, already installed)

else # Linux
    # Install pyenv
    wget -qO- https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
    export PATH="/home/travis/.pyenv/bin:$PATH"
fi

eval "$(pyenv init -)"
pyenv install 3.5.2
pyenv global 3.5.2

pip install --upgrade pip
pip install --upgrade setuptools
