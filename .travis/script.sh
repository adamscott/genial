#!/usr/bin/env bash
set -ex

# Initialize pyenv
eval "$(pyenv init -)"
pyenv global 3.5.2

LRELEASE=/opt/qt57/bin/lrelease

python setup.py bootstrap --lrelease=$LRELEASE
echo "===   TEST   ==="
/home/travis/.pyenv/versions/3.5.2/bin/py.test --cov=genial/ tests/
echo "=== END TEST ==="
python setup.py test
