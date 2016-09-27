#!/usr/bin/env bash
set -e

source colors.sh

echo -e "${COLOR[lightyellow_fg]}=> Setup pyenv${COLOR[default_fg]}"

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    echo -e "${COLOR[lightyellow_fg]}==> Uninstalling outdated pyenv${COLOR[default_fg]}"
    brew uninstall pyenv  # uninstall outdated pyenv
fi

echo -e "${COLOR[lightyellow_fg]}==> Installing pyenv${COLOR[default_fg]}"
wget -qO- https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

# Makes builds a little faster
export PYTHON_CFLAGS='-O2'

# Inits pyenv
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Python version to build
python_version="3.5.2"

# Log name
python_build_log="python-${python_version}-${TRAVIS_OS_NAME}.log"

# Installs and sets global python to v3.5.2
echo -e "${COLOR[lightyellow_fg]}==> Install python 3.5.2${COLOR[default_fg]}"
pyenv install --verbose "${python_version}" &>"${python_build_log}"
echo -e "${COLOR[lightyellow_fg]}==> Set global python version to 3.5.2${COLOR[default_fg]}"
pyenv global "${python_version}"

# Update gist
echo -e "${COLOR[lightyellow_fg]}==> Sending logs to gist${COLOR[default_fg]}"
gist -u 1519c3ffb6bcccdf40223563f3a84448 "${python_build_log}"

# Get the latest version of pip and setuptools, which both come preinstalled, but outdated
pip install --upgrade pip
pip install --upgrade setuptools
