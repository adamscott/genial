#!/usr/bin/env bash
set -ex

# Initialize pyenv
eval "$(pyenv init -)"
pyenv global 3.5.2

LRELEASE=/opt/qt57/bin/lrelease

python setup.py bootstrap --lrelease=$LRELEASE
set +e # Disable temporarily exit on error
python setup.py test
set -e # Reenable exit on error