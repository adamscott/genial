#!/usr/bin/env bash
set -ex

# Initialize pyenv
eval "$(pyenv init -)"
pyenv global 3.5.2

LRELEASE=/opt/qt57/bin/lrelease

python setup.py bootstrap --lrelease=$LRELEASE
python setup.py test
