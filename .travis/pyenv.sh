#!/usr/bin/env bash
set -e

source helpers.sh

log_verbose "=> Setup pyenv"

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    log_verbose "==> Uninstalling outdated pyenv"
    brew uninstall pyenv  # uninstall outdated pyenv
fi

log_verbose "==> Installing pyenv"
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
log_verbose "==> Install python 3.5.2"
pyenv install --verbose "${python_version}" &>"${python_build_log}"
log_verbose "==> Set global python version to 3.5.2 (and coloredlogs/verboselogs install right after)"
pyenv global "${python_version}"

# Update gist
log_verbose "==> Sending logs to gist"
gist -u 1519c3ffb6bcccdf40223563f3a84448 "${python_build_log}"

# Get the latest version of pip and setuptools, which both come preinstalled, but outdated
log_verbose "==> Updating pip"
pip install --upgrade pip
log_verbose "==> Updating setuptools"
pip install --upgrade setuptools
