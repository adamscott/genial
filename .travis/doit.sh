#!/usr/bin/env bash
set -e

source colors.sh

echo -e "${COLOR[lightyellow_fg]}==> Installing doit${COLOR[default_fg]}"
pip install doit
