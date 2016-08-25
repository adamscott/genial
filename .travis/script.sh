#!/usr/bin/env bash
set -ex

# Initialize pyenv
eval "$(pyenv init -)"
pyenv global 3.5.2

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then
    # Install some custom requirements on OS X
    export LRELEASE=/usr/local/Cellar/qt5/5.6.1-1/bin/lrelease
else

fi

python setup.py bootstrap
python setup.py test