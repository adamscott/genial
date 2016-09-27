#!/usr/bin/env bash
set -e

source colors.sh

echo -e "${COLOR[lightyellow_fg]}=> Setup packages${COLOR[default_fg]}"

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    echo -e "${COLOR[lightyellow_fg]}==> Updating brew${COLOR[default_fg]}"
    brew update

    # pyenv dependencies
    echo -e "${COLOR[lightyellow_fg]}==> Installing autoconf${COLOR[default_fg]}"
    brew install autoconf
    echo -e "${COLOR[lightyellow_fg]}==> Installing openssl${COLOR[default_fg]}"
    brew install openssl
    echo -e "${COLOR[lightyellow_fg]}==> Installing readline${COLOR[default_fg]}"
    brew install readline
    echo -e "${COLOR[lightyellow_fg]}==> Installing xz${COLOR[default_fg]}"
    brew install xz

    # needed to convert .md to .rst
    echo -e "${COLOR[lightyellow_fg]}==> Installing pandoc${COLOR[default_fg]}"
    brew install pandoc
fi
# No need to setup packages in Linux build
