#!/usr/bin/env bash
set -e

source helpers.sh

log_verbose "=> Setup packages"

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    log_verbose "==> Updating brew"
    brew update

    # pyenv dependencies
    log_verbose "==> Installing autoconf"
    brew install autoconf
    log_verbose "==> Installing openssl"
    brew install openssl
    log_verbose "==> Installing readline"
    brew install readline
    log_verbose "==> Installing xz"
    brew install xz

    # needed to convert .md to .rst
    log_verbose "==> Installing pandoc"
    brew install pandoc
fi
# No need to setup packages in Linux build
